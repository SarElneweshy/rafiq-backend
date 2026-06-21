from django.db import migrations

def load_initial_data(apps, schema_editor):
    Disorder = apps.get_model('exercises', 'Disorder')
    Exercise = apps.get_model('exercises', 'Exercise')
    disorders_data = [

        {"pk": 1, "short_name": "MDD", "full_name": "Major Depressive Disorder"},
        {"pk": 2, "short_name": "ASD", "full_name": "Autism Spectrum Disorder"},
        {"pk": 3, "short_name": "Loneliness", "full_name": "Loneliness"},
        {"pk": 4, "short_name": "Bipolar", "full_name": "Bipolar Disorder"},
        {"pk": 5, "short_name": "Anxiety", "full_name": "Anxiety"},
        {"pk": 6, "short_name": "PTSD", "full_name": "Post-Traumatic Stress Disorder"},
        {"pk": 7, "short_name": "Sleeping", "full_name": "Sleeping Disorder"},
        {"pk": 8, "short_name": "Psychotic", "full_name": "Psychotic Depression"},
        {"pk": 9, "short_name": "Eating", "full_name": "Eating Disorder"},
        {"pk": 10, "short_name": "ADHD", "full_name": "Attention-Deficit/Hyperactivity Disorder"},
        {"pk": 11, "short_name": "PDD", "full_name": "Persistent Depressive Disorder"},
        {"pk": 12, "short_name": "OCD", "full_name": "Obsessive-Compulsive Disorder"},
    ]
    disorder_objects = {}
    for d in disorders_data:
        obj, _ = Disorder.objects.get_or_create(
            id=d["pk"],
            defaults={"short_name": d["short_name"], "full_name": d["full_name"]}
        )
        disorder_objects[d["pk"]] = obj
    exercises_data = [
        {
 "pk": 1, "disorder_id": 1, "title": "Major Depressive Disorder",
 "short": "Write a short note to your future self, reminding them that healing takes time.",
 "detail": "Write to your future self: Take a note and write a short message to yourself 3 or 6 months from now — remind yourself that healing takes time and small steps count.\nDeep breathing: Sit quietly, take 5 slow breaths. Inhale for 3 counts, exhale slowly.",
 "video": "https://www.youtube.com/watch?v=inpok4MKVLM"
        },
        {
"pk": 2, "disorder_id": 2, "title": "Autism Spectrum Disorder",
"short": "Spend two minutes organizing around you; order can make your mind feel safe.",
"detail": "Organize a small area: Spend 2 minutes arranging something simple like your desk or a small shelf — structure helps calm sensory overload\nCalming sounds: Listen to gentle, slow music or nature sounds while sitting quietly.",
"video": "https://youtu.be/4Talws29mys?si=Ec6dniPHrLkXwwkK"
        },
        {
"pk": 3, "disorder_id": 3, "title": "Loneliness",
"short": "Listen to a song that makes you feel connected or brings good memories.",
"detail": "Send a kind message: Text someone you care about — “I thought of you today.” Simple connection helps reduce loneliness.\nJournal your feelings: Write “I feel…” and “I wish…” — express your emotions without judging them.",
"video": "https://youtu.be/GckT5n9Ik1s"
        },
        {
"pk": 4, "disorder_id": 4, "title": "Bipolar Disorder",
"short": "Draw or color something that matches how your mood feels right now.",
"detail": "Mood tracking: Write “Mood right now:” and “Energy level:” — this helps notice mood patterns.\nShort walk or stretching: Move your body gently to release stress and regulate emotions.",
"video": "https://www.youtube.com/watch?v=inpok4MKVLM"
        },
        {
"pk": 5, "disorder_id": 5, "title": "Anxiety",
"short": "Hold something small in your hand and describe it in detail — focus on its texture, color, and shape.",
"detail": "5-4-3-2-1 grounding: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste — brings you back to the present moment.\nBox breathing: Inhale 4 counts, hold 4, exhale 4 — repeat for a minute.",
"video": "https://youtu.be/SNqYG95j_UQ"
        },

        {
"pk": 6, "disorder_id": 6, "title": "PTSD",
"short": "Wrap yourself in a blanket or hug a pillow — remind your body it’s safe now.",
"detail": "Name 3 safe things: Look around and identify “something safe I see,” “something safe I can touch,” “something safe I hear.”\nNature sounds: Play calming sounds (waves, rain, forest) for 2–3 minutes — focus only on the sound.",
"video": "https://www.youtube.com/watch?v=VDLfVwMSbJ8"
        },
        {
"pk": 7, "disorder_id": 7, "title": "Sleeping Disorder",
"short": "Write down three thoughts from your mind before bed to clear your head.",
"detail": "No screens before bed: Turn off screens 15 minutes before sleeping and lower the lights.\nBedtime relaxation: Lie down, breathe slowly, and listen to soft sounds or a sleep meditation.",
"video": "https://www.youtube.com/watch?v=ywTaRqSbQpw"
        },
        {
"pk": 8, "disorder_id": 8, "title": "Psychotic Depression",
"short": "Say out loud one sentence that keeps you grounded in reality, like “I’m safe in my room right now”.",
"detail": "Reality check list: Write two lines — “This is real:” and “This is just a thought:” — helps you separate facts from mental noise.\nGround through touch: Hold a chair or feel the floor — focus on physical sensation.",
"video": "https://www.youtube.com/watch?v=qKcRUOWYQ9w"
        },
        {
"pk": 9, "disorder_id": 9, "title": "Eating Disorder",
"short": "Before your next meal, take one deep breath and thank your body for supporting you.",
"detail": "Mindful gratitude: Before eating, pause and say “I thank my body for working today.\nSlow eating: Focus on the taste, smell, and texture of each bite — without judgment.",
"video": "https://www.youtube.com/watch?v=LiUnFJ8P4gM"
        },
        {
"pk": 10, "disorder_id": 10, "title": "ADHD",
"short": "Pick one simple task and set a fun 5-minute timer — focus until it ends.",
"detail": "10-minute timer: Set a timer for 10 minutes and focus on one small task only.\nTop 3 goals: Write three things you want to achieve today \n — keeps your focus structured",
"video": "https://www.youtube.com/watch?v=rTIv5X8Bo1w"
        },
        {
"pk": 11, "disorder_id": 11, "title": "PDD",
"short": "Stand near a window and notice one thing that looks alive — light, a tree, or movement.",
"detail": "Move your body: Stretch or walk for 2 minutes to activate energy.\nSet one tiny goal: “Drink an extra glass of water” or “Read one page” — celebrate completing it.",
"video": "https://www.youtube.com/watch?v=LiUnFJ8P4gM"
        },
        {
"pk": 12, "disorder_id": 12, "title": "OCD",
"short": "When the urge comes, gently tap your fingers five times instead — remind yourself you’re in control.",
"detail": "Delay the urge: When you feel a compulsion, breathe slowly for 2 minutes before acting.\n Focus on one sound: Pick a soft noise (fan, clock, or music) and listen to it carefully for a few minutes. ",
"video": "https://www.youtube.com/watch?v=pxWOpGm4d7U"
        }
    ]
    for ex in exercises_data:
        Exercise.objects.get_or_create(
            id=ex["pk"],
            defaults={
 "disorder": disorder_objects[ex["disorder_id"]],
 "title": ex["title"],
 "short_desc": ex["short"],
 "detailed_desc": ex["detail"],
 "video_url": ex["video"]
            }
        )
def unload_initial_data(apps, schema_editor):
    Disorder = apps.get_model('exercises', 'Disorder')
    Exercise = apps.get_model('exercises', 'Exercise')
    Exercise.objects.all().delete()
    Disorder.objects.all().delete()
class Migration(migrations.Migration):
    dependencies = [
        ('exercises', '0001_initial'), 
    ]
    operations = [
        migrations.RunPython(load_initial_data, unload_initial_data),
    ]