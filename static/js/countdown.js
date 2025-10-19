(function(){
  const d = document.getElementById("d");
  const h = document.getElementById("h");
  const m = document.getElementById("m");
  const s = document.getElementById("s");
  const daysInline = document.getElementById("days");
  const hoursInline = document.getElementById("hours");
  const minutesInline = document.getElementById("minutes");
  const secondsInline = document.getElementById("seconds");
  const celebrate = document.getElementById("celebrate");
  const clientTz = document.getElementById("client-tz");

  function pad(n){ return n.toString().padStart(2,'0'); }

  function targetFor(now){
    const y = now.getMonth() > 11 || (now.getMonth() === 11 && now.getDate() > 25) ? now.getFullYear() + 1 : now.getFullYear();
    return new Date(y, 11, 25, 0, 0, 0); // 25 de dic, 00:00 local
  }

  function update(){
    const now = new Date();
    const target = targetFor(now);
    const ms = target - now;

    if (clientTz && Intl && Intl.DateTimeFormat) {
      try { clientTz.textContent = "Tu zona horaria: " + Intl.DateTimeFormat().resolvedOptions().timeZone; } catch(e){}
    }

    if (ms <= 0){
      if (celebrate) celebrate.hidden = false;
      [d,h,m,s].forEach(el => { if (el) el.textContent = "0"; });
      [daysInline,hoursInline,minutesInline,secondsInline].forEach(el => { if (el) el.textContent = "0"; });
      return;
    }

    const totalSeconds = Math.floor(ms/1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    if (d) d.textContent = days.toString();
    if (h) h.textContent = pad(hours);
    if (m) m.textContent = pad(minutes);
    if (s) s.textContent = pad(seconds);

    if (daysInline) daysInline.textContent = days.toString();
    if (hoursInline) hoursInline.textContent = hours.toString();
    if (minutesInline) minutesInline.textContent = minutes.toString();
    if (secondsInline) secondsInline.textContent = seconds.toString();
  }

  update();
  setInterval(update, 1000);
})();