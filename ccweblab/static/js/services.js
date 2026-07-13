document.addEventListener("DOMContentLoaded", () => {
  const featureModal = document.getElementById("featureModal");
  const featureTitle = document.getElementById("featureModalTitle");
  const featureSubtitle = document.getElementById("featureModalSubtitle");
  const featureContent = document.getElementById("featureContent");

  const pricingModal = document.getElementById("pricingModal");
  const pricingTitle = document.getElementById("modalTitle");
  const pricingSubtitle = document.getElementById("modalSubtitle");
  const planRow = document.getElementById("planRow");

  function escapeHtml(str){
    return String(str)
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  // PRICING DATA
  const serviceTitles = {
    dev: "Website Development Plans",
    ecom: "E‑commerce Plans",
    maint: "Maintenance & Updates Plans",
    geo: "Indoor Geo Location App Plans",
    book: "Booking & Reservation App Plans",
    analytics: "Data Analytics Plans",
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
    analytics: [
      { name:"Basic Plan", tag:"Getting started", price:"Starting at €800", includes:["Dashboard setup","Basic reporting","Data visualization","Monthly insights","Support"] },
      { name:"Standard Package", tag:"Most popular", featured:true, price:"Starting at €1,500", includes:["Advanced analytics","Custom reports","Real-time dashboards","Predictive insights","Priority support"] },
      { name:"Premium Package", tag:"Enterprise insights", price:"Starting at €2,500", includes:["AI-powered analytics","Custom integrations","Advanced segmentation","Dedicated analyst","24/7 support"] },
    ],
  };

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

  function openPricingModal(serviceKey){
    pricingTitle.textContent = serviceTitles[serviceKey] || "Plans";
    pricingSubtitle.textContent = "Compare packages and choose what fits your goals.";
    const plans = plansByService[serviceKey] || [];
    planRow.innerHTML = plans.map(planToHTML).join("");
    pricingModal.classList.add("is-open");
    pricingModal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closePricingModal(){
    pricingModal.classList.remove("is-open");
    pricingModal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  // FEATURE DATA
  const featureData = {
    websites: {
      title: "Custom Websites",
      subtitle: "Bespoke, high-converting websites designed to elevate your brand",
      description: "Our custom website solutions are tailored to your brand's unique identity and business goals. We create high-converting websites that attract and engage your ideal clients.",
      features: [
        "Responsive design that looks perfect on all devices",
        "Fast-loading optimized pages",
        "SEO-optimized structure",
        "CMS integration for easy content management",
        "Custom functionality tailored to your needs"
      ]
    },
    booking: {
      title: "Booking Software",
      subtitle: "Powerful booking and client management",
      description: "Streamline your appointment scheduling with our intuitive booking software. Reduce no-shows, manage availability, and provide a seamless client experience.",
      features: [
        "Easy online appointment scheduling",
        "Automated confirmation & reminder emails",
        "Client database management",
        "Calendar synchronization",
        "Payment integration"
      ]
    },
    experience: {
      title: "Client Experience",
      subtitle: "Seamless digital experiences for your clients",
      description: "Transform how your clients interact with your business. Our solutions make booking, managing services, and staying connected effortless.",
      features: [
        "Intuitive user interface",
        "Self-service portal for clients",
        "Automated communications",
        "Mobile-friendly design",
        "Personalized client journeys"
      ]
    },
    growth: {
      title: "Business Growth",
      subtitle: "Conversion-focused design and tools",
      description: "Scale your business sustainably with tools and strategies designed to drive growth. From conversion optimization to client retention, we've got you covered.",
      features: [
        "Conversion rate optimization",
        "Analytics and reporting",
        "Client retention strategies",
        "Marketing automation",
        "Growth consulting"
      ]
    },
    support: {
      title: "Ongoing Support",
      subtitle: "Reliable support and maintenance",
      description: "We're here when you need us. Our dedicated support team ensures your business stays ahead with proactive maintenance and responsive assistance.",
      features: [
        "24/7 technical support",
        "Regular updates and maintenance",
        "Security monitoring",
        "Performance optimization",
        "Proactive issue resolution"
      ]
    }
  };

  function openFeatureModal(featureKey){
    const data = featureData[featureKey];
    if (!data) return;

    featureTitle.textContent = data.title;
    featureSubtitle.textContent = data.subtitle;

    const featureHTML = `
      <h3>${escapeHtml(data.description)}</h3>
      <ul>
        ${data.features.map(f => `<li>${escapeHtml(f)}</li>`).join('')}
      </ul>
    `;

    featureContent.innerHTML = featureHTML;
    featureModal.classList.add("is-open");
    featureModal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeFeatureModal(){
    featureModal.classList.remove("is-open");
    featureModal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  // Map feature keys to service keys for pricing
  const featureToServiceMap = {
    websites: "dev",
    booking: "book",
    experience: "book",
    growth: "ecom",
    support: "maint"
  };

  // Feature card click handlers - open pricing modal
  document.querySelectorAll(".feature-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const featureKey = btn.dataset.feature;
      const serviceKey = featureToServiceMap[featureKey];
      if (serviceKey) {
        openPricingModal(serviceKey);
      }
    });
  });

  // Service card click handlers - open pricing modal
  document.querySelectorAll(".service-card").forEach(btn => {
    btn.addEventListener("click", () => {
      const serviceMap = {
        websites: "dev",
        booking: "book",
        ecommerce: "ecom",
        analytics: "analytics",
        gps: "geo"
      };
      const serviceKey = serviceMap[btn.dataset.service];
      if (serviceKey) {
        openPricingModal(serviceKey);
      }
    });
  });

  // Modal backdrop and close button handlers
  featureModal?.addEventListener("click", (e) => {
    if (e.target?.dataset?.close === "true") closeFeatureModal();
    if (e.target === featureModal) closeFeatureModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && featureModal.classList.contains("is-open")) closeFeatureModal();
  });

  // Pricing modal event listeners
  document.querySelectorAll(".svc-btn").forEach(btn => {
    btn.addEventListener("click", () => openPricingModal(btn.dataset.service));
  });

  pricingModal?.addEventListener("click", (e) => {
    if (e.target?.dataset?.close === "true") closePricingModal();
    if (e.target === pricingModal) closePricingModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && pricingModal.classList.contains("is-open")) closePricingModal();
  });

  // Process step click handlers - expand/collapse
  document.querySelectorAll(".process-step").forEach(step => {
    step.addEventListener("click", () => {
      const isExpanded = step.classList.contains("expanded");
      
      // Close all other steps
      document.querySelectorAll(".process-step").forEach(s => {
        s.classList.remove("expanded");
      });
      
      // Toggle current step
      if (!isExpanded) {
        step.classList.add("expanded");
      }
    });
  });

  // reveal animation
  const observer = new IntersectionObserver((entries)=>{
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add("in");
    });
  }, { threshold: 0.14 });

  document.querySelectorAll("section, .card, .feature-btn, .svc-btn, .service-card, .process-step").forEach(el => {
    el.classList.add("reveal");
    observer.observe(el);
  });
});