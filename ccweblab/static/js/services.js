document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("pricingModal");
  const planRow = document.getElementById("planRow");
  const title = document.getElementById("modalTitle");
  const subtitle = document.getElementById("modalSubtitle");

  const serviceTitles = {
    dev: "Website Development Plans",
    ecom: "E‑commerce Plans",
    maint: "Maintenance & Updates Plans",
    geo: "Indoor Geo Location App Plans",
    book: "Booking & Reservation App Plans",
  };

  const plansByService = {
    dev: [
      { name:"Basic Plan", tag:"Best for: landing page", price:"Starting at €500", includes:["1 landing page","Responsive design","Contact form","Basic SEO","Launch support"] },
      { name:"Standard Package", tag:"Most popular", featured:true, price:"Starting at €1,000", includes:["Up to 5 pages","Custom design","Speed optimization","SEO setup","Analytics"] },
      { name:"Premium Package", tag:"Growth-ready", price:"Starting at €2,000", includes:["Up to 10 pages","CMS/blog","Advanced performance","Accessibility","Priority support"] },
    ],
    ecom: [
      { name:"Basic Plan", tag:"Small store", price:"Starting at €900", includes:["Store setup","Up to 10 products","Payments setup","Theme customization","Launch support"] },
      { name:"Standard Package", tag:"Most popular", featured:true, price:"Starting at €1,800", includes:["Up to 30 products","Shipping/tax setup","Automation basics","SEO foundations","Performance optimization"] },
      { name:"Premium Package", tag:"Scale-ready", price:"Starting at €3,000", includes:["Custom sections","Integrations","Conversion UX","Advanced tracking","Priority support"] },
    ],
    maint: [
      { name:"Basic Plan", tag:"Keep it stable", price:"€120 / month", includes:["Monthly updates","Backups","Security checks","1 content change","Email support"] },
      { name:"Standard Package", tag:"Most popular", featured:true, price:"€250 / month", includes:["Weekly updates","Monitoring","Performance checks","4 content changes","Priority support"] },
      { name:"Premium Package", tag:"Business critical", price:"€450 / month", includes:["Proactive monitoring","Security hardening","Speed optimization","Unlimited minor edits","Fast SLA"] },
    ],
    geo: [
      { name:"Basic Plan", tag:"Indoor navigation", price:"Starting at €2,500", includes:["Real-time indoor positioning","Venue maps","Wayfinding UI","System integration","Support"] },
      { name:"Standard Package", tag:"Most popular", featured:true, price:"Starting at €4,000", includes:["Advanced navigation","Admin controls","Analytics","API integration","Priority support"] },
      { name:"Premium Package", tag:"Enterprise", price:"Starting at €7,000", includes:["Custom architecture","Multi-venue support","Deep integration","Custom dashboards","Dedicated support"] },
    ],
    book: [
      { name:"Basic Plan", tag:"Essentials", price:"Starting at €1,200", includes:["Online booking","Calendar integration","Email notifications","Simple admin panel","Support"] },
      { name:"Standard Package", tag:"Most popular", featured:true, price:"Starting at €2,200", includes:["Multi-service booking","Availability rules","Reminders","Reporting","Priority support"] },
      { name:"Premium Package", tag:"All-inclusive", price:"Starting at €3,800", includes:["Advanced scheduling","Custom workflows","Roles/permissions","Analytics","Dedicated support"] },
    ],
  };

  function escapeHtml(str){
    return String(str)
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  function planToHTML(p){
    const li = (p.includes || []).map(x => `<li>${escapeHtml(x)}</li>`).join("");
    return `
      <article class="plan ${p.featured ? "featured" : ""}">
        <div class="tag">${escapeHtml(p.tag || "")}</div>
        <h3>${escapeHtml(p.name)}</h3>
        <ul>${li}</ul>
        <div class="price">${escapeHtml(p.price || "")}</div>
        <div class="cta">
          <a class="btn primary" href="#contact" data-close="true">Choose this plan</a>
        </div>
      </article>
    `;
  }

  function openModal(serviceKey){
    title.textContent = serviceTitles[serviceKey] || "Plans";
    subtitle.textContent = "Compare packages and choose what fits your goals.";
    const plans = plansByService[serviceKey] || [];
    planRow.innerHTML = plans.map(planToHTML).join("");
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeModal(){
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  document.querySelectorAll(".svc-btn").forEach(btn => {
    btn.addEventListener("click", () => openModal(btn.dataset.service));
  });

  modal?.addEventListener("click", (e) => {
    if (e.target?.dataset?.close === "true") closeModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("is-open")) closeModal();
  });

  // reveal animation
  const observer = new IntersectionObserver((entries)=>{
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add("in");
    });
  }, { threshold: 0.14 });

  document.querySelectorAll("section, .card, .svc-btn").forEach(el => {
    el.classList.add("reveal");
    observer.observe(el);
  });
});