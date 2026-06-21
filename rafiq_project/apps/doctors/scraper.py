import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.utils import timezone
from .models import Doctor, ScrapingLog

CITY_SLUGS = {
    'cairo'           : 'Cairo',      
    'alexandria'      : 'Alexandria',
    'giza'            : 'Giza',
    'assiut'          : 'Assiut',
    'el-sharqia'      : 'El-Sharqia',
    'el-ismailia'     : 'El-Ismailia',
    'matrouh'         : 'Matrouh',
    'el-dakahlia'     : 'El-Dakahlia',
    'el-beheira'      : 'El-Beheira',
    'damietta'        : 'Damietta',
    'north-coast'     : 'North Coast',
    'qalyubia'        : 'Qalyubia',
    'gharbia'         : 'Gharbia',
    'menoufia'        : 'Menoufia',
    'fayoum'          : 'Fayoum',
    'hurghada'        : 'Hurghada',
    'sharm-el-sheikh' : 'Sharm El Sheikh',
    'port-said'       : 'Port Said',
    'suez'            : 'Suez',
    'sohag'           : 'Sohag',
    'el-minia'        : 'El-Minia',
    'kafr-el-sheikh'  : 'Kafr El Sheikh',
    'luxor'           : 'Luxor',
    'qena'            : 'Qena',
    'aswan'           : 'Aswan',
    'beni-suef'       : 'Beni Suef',
}
BASE_URL = 'https://www.vezeeta.com'

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

def parse_card(card, city_name):
    try:
        try:
            script_el = card.find_element(
                By.CSS_SELECTOR, 'script[type="application/ld+json"]'
            )
            json_ld = json.loads(script_el.get_attribute('innerHTML'))
        except Exception:
            return None

        url_path = json_ld.get('url', '').strip()
        if not url_path:
            return None
        if is_arabic(url_path):
            return None
        vezeeta_url = (
            f'{BASE_URL}{url_path}'
            if url_path.startswith('/') else url_path
        )

        #3. name

        name = json_ld.get('name', '').strip()
        if not name or is_arabic(name):
            return None
        if is_arabic(name):
            return None
        #4. sub_specialty
        sub_specialty = json_ld.get('description', '').strip()
        if is_arabic(sub_specialty):
            sub_specialty = ''

        # ── 5. area
        area = json_ld.get('areaServed', '').strip()
        if is_arabic(area):
            area = ''

        # ── 6. address
        address = ''
        try:
            address = card.find_element(
                By.CSS_SELECTOR, '[itemprop="address"]'
            ).text.strip()
        except Exception:
            pass
        if is_arabic(address):
            address = ''
        if not address:
            address = area
        # ── 7. price
        price = None
        price_str = json_ld.get('priceRange', '')
        if price_str:
            digits = ''.join(filter(str.isdigit, price_str))
            price  = int(digits) if digits else None
        #8. Image
        image_url = json_ld.get('image', '').strip()
        if is_arabic(image_url):
            image_url = ''

        # ── 9. Rating 

        rating = None
        try:
            testid = card.find_element(
                By.CSS_SELECTOR,
                '[data-testid*="star-rating__rating-value"]'
            ).get_attribute('data-testid')or ''
            match  = re.search(r'(\d+\.?\d*)$', testid)
            if match:
                rating = float(match.group(1))
        except Exception:
            pass

        # ── 10. reviews 
        reviews_count = 0
        try:
            text   = card.find_element(
                By.XPATH, './/*[contains(text(),"Visitors")]'
            ).text
            digits = ''.join(filter(str.isdigit, text.split('Visitors')[0]))
            reviews_count = int(digits) if digits else 0
        except Exception:
            pass

        return {
            'name'          : name,
            'sub_specialty' : sub_specialty,
            'city'          : city_name,
            'area'          : area,
            'address'       : address,
            'rating'        : rating,
            'reviews_count' : reviews_count,
            'price'         : price,
            'image_url'     : image_url,
            'vezeeta_url'   : vezeeta_url,
            'is_active'      : True,
        }

    except Exception:
        return None
    
def get_cards(driver):
   return [
        card for card in driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="doctor-card-"]'
        )
        if re.match(
            r'^doctor-card-\d+$',
            card.get_attribute('data-testid') or ''
        )
    ]

def scrape_city(city_slug, city_name, log=print):
    driver       = get_driver()
    page         = 1
    saved        = 0
    updated      = 0
    deactivated   = 0
    seen_urls    = set()
    scraping_log = ScrapingLog.objects.create(city=city_name, status='partial')

    try:
        while True:
            log(f'[{city_name}] Page {page}')
            driver.get(f'{BASE_URL}/en/doctor/psychiatry/{city_slug}?page={page}')
            time.sleep(4)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        '[data-testid^="doctor-card-"]'
                    ))
                )
            except Exception:
                log(f'[{city_name}] No more pages at {page}')
                break
            time.sleep(2)
            cards = get_cards(driver)
            if not cards:
                break
            log(f'{len(cards)} doctors found')
            page_saved = 0

            for card in cards:
                data = parse_card(card, city_name)
                if not data:
                    continue

                seen_urls.add(data['vezeeta_url'])
                _, created = Doctor.objects.update_or_create(
                    vezeeta_url=data['vezeeta_url'],
                    defaults=data,
                )
                if created:
                    saved      += 1
                    page_saved += 1
                else:
                    updated += 1

            log(f'New: {page_saved} | Total: {saved}')
            page += 1
            time.sleep(3)

        if seen_urls:
            deactivated = (
                Doctor.objects
                .filter(city__iexact=city_name)
                .exclude(vezeeta_url__in=seen_urls)
                .update(is_active=False)
            )
            if deactivated:
                log(f'Deactivated {deactivated}')

        scraping_log.status      = 'success'
        scraping_log.saved       = saved
        scraping_log.updated     = updated
        scraping_log.deactivated = deactivated
        scraping_log.finished_at = timezone.now()
        scraping_log.save()

        log(f'[{city_name}] Done! Saved: {saved} | Updated: {updated}')

    except Exception as e:
        scraping_log.status      = 'failed'
        scraping_log.error       = str(e)
        scraping_log.finished_at = timezone.now()
        scraping_log.save()
        log(f'[{city_name}] Error: {e}')

    finally:
        driver.quit()

    return saved, updated, deactivated


def scrape_all(city_slug='egypt', log=print):
    if city_slug == 'egypt':
        total_saved = 0
        total_updated = 0
        total_deactivated = 0

        for slug, name in CITY_SLUGS.items():
            log(f'\n Starting city: {name}')
            s, u, d = scrape_city(slug, name, log)
            total_saved       += s
            total_updated     += u
            total_deactivated += d

        log(f'\n ALL DONE | Saved: {total_saved} | Updated: {total_updated} | Deactivated: {total_deactivated}')
        return total_saved, total_updated

    city_name = CITY_SLUGS.get(city_slug, city_slug.replace('-', ' ').title())
    s, u, d  = scrape_city(city_slug, city_name, log)
    return s, u