// static/js/auth/login.js
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('login-form');
  const msg = document.getElementById('msg');

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function getCsrfToken() {
    // 1) try cookie
    let token = getCookie('csrftoken');
    if (token) return token;

    // 2) fallback: read hidden input produced by {% csrf_token %}
    const input = form.querySelector('input[name="csrfmiddlewaretoken"]');
    if (input) return input.value;

    return null;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    msg.textContent = '';
    msg.classList.remove('success');

    // build form-encoded payload
    const payload = new URLSearchParams();
    // If backend expects "email" instead of "username" change the key here.
    payload.append('email', form.email.value.trim());
    payload.append('password', form.password.value);

    const csrftoken = getCsrfToken();
    console.log('csrftoken:', csrftoken);

    try {
      const res = await fetch('/api/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          ...(csrftoken ? {'X-CSRFToken': csrftoken} : {})
        },
        credentials: 'same-origin', // ensure cookies are sent
        body: payload.toString()
      });

      // try parse JSON, fallback to text for debugging
      let json;
      try {
        json = await res.json();
      } catch (err) {
        const txt = await res.text();
        console.warn('Non-JSON response:', res.status, txt);
        throw { detail: `Server error ${res.status}: ${txt}` };
      }

      if (!res.ok) throw json;

      // save token (token field might be 'token' or 'key' depending on your backend)
      const token = json.token || json.key || '';
      if (token) localStorage.setItem('authToken', token);

      // fetch profile if endpoint exists
      try {
        const profileRes = await fetch('/api/accounts/profile/', {
          headers: { 'Authorization': 'Token ' + token },
          credentials: 'same-origin'
        });
        if (profileRes.ok) {
          const user = await profileRes.json();
          localStorage.setItem('user', JSON.stringify(user));
        }
      } catch (e) {
        console.warn('Profile fetch failed:', e);
      }

      msg.textContent = 'Signed in successfully — redirecting...';
      msg.classList.add('success');

      // // redirect (عدل المسار لو مطلوب)
      // window.location.href = '/templates/profile.html';

    } catch (err) {
      console.error('Login error:', err);
      msg.textContent = err.detail || err.non_field_errors?.[0] || err.message || 'Login failed. Please check your credentials.';
    }
  });
});
