document.addEventListener('DOMContentLoaded', ()=> {
  const form = document.getElementById('signup-form');
  const msg  = document.getElementById('msg');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    msg.textContent = '';

    const body = {
      email: form.email.value.trim(),
      first_name: form.first_name.value.trim(),
      last_name: form.last_name.value.trim(),
      password: form.password.value
    };

    try {
      const res = await fetch('/api/accounts/signup/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json().catch(()=>({}));
      if (!res.ok) {
        // show API validation errors or general message
        msg.textContent = data.detail || (data.email?.join?.(', ') || JSON.stringify(data));
        return;
      }
      // success: save token & redirect
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      window.location.href = '/accounts/profile/';
    } catch (err) {
      msg.textContent = err.detail || err.message || 'Sign up failed';
    }
  });
});