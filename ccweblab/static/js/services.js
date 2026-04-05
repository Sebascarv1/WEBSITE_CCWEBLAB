// services/static/js/services.js
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("pricingModal");
  const planRow = document.getElementById("planRow");
  const title = document.getElementById("modalTitle");
  const subtitle = document.getElementById("modalSubtitle");

  const serviceTitles = {
    dev: "Website Development Plans",
    ecom: "E‑commerce Plans",
    maint: "Maintenance & Updates Plans",
  };

  // You can customize per service here
  const plansByService = {
    dev: [
      {
        name: "Basic Plan",
        tag: "Best for: 1-page landing",
        price: "Starting at $___",
        includes: [
          "1 landing page",
          "Mobile responsive design",
          "Contact form",
          "Basic SEO setup",
          "Deploy & launch support",
        ],
      },
      {
        name: "Normal Package",
        tag: "Most popular",
        featured: true,
        price: "Starting at $___",
        includes: [
          "Up to 5 pages",
          "Custom design + animations",
          "Speed optimization",
          "SEO foundations + sitemap",
          "Google Analytics setup",
        ],
      },
      {
        name: "Premium Package",
        tag: "Best for: business growth",
        price: "Starting at $___",
        includes: [
          "Up to 10 pages",
          "Blog or CMS integration",
          "Advanced performance + accessibility",
          "On-page SEO improvements",
          "30 days priority support",
        ],
      },
    ],
    ecom: [
      {
        name: "Basic Plan",
        tag: "Small store",
        price: "Starting at $___",
        includes: [
          "Store setup (Shopify or similar)",
          "Up to 10 products",
          "Payments setup",
          "Basic theme customization",
          "Launch support",
        ],
      },
      {
        name: "Normal Package",
        tag: "Most popular",
        featured: true,
        price: "Starting at $___",
        includes: [
          "Up to 30 products",
          "Collections + product variants",
          "Shipping & tax setup",
          "Email capture + basic automation",
          "Speed + SEO foundations",
        ],
      },
      {
        name: "Premium Package",
        tag: "Scale-ready",
        price: "Starting at $___",
        includes: [
          "Unlimited products (platform-dependent)",
          "Custom sections/components",
          "Conversion-focused UX",
          "Integrations (reviews, CRM, pixels)",
          "30 days priority support",
        ],
      },
    ],
    maint: [
      {
        name: "Basic Plan",
        tag: "Keep it updated",
        price: "$___ / month",
        includes: [
          "Monthly updates",
          "Backups",
          "Basic security checks",
          "1 content change/month",
          "Email support",
        ],
      },
      {
        name: "Normal Package",
        tag: "Most popular",
        featured: true,
        price: "$___ / month",
        includes: [
          "Weekly updates",
          "Uptime monitoring",
          "Performance checks",
          "Up to 4 content changes/month",
          "Priority email support",
        ],
      },
      {
        name: "Premium Package",
        tag: "Business critical",
        price: "$___ / month",
        includes: [
          "Proactive monitoring",
          "Speed optimization",
          "Security hardening",
          "Unlimited small edits (fair use)",
          "Priority support + faster SLA",
        ],
      },
    ],
  };

  function openModal(serviceKey){
    title.textContent = serviceTitles[serviceKey] || "Plans";
    subtitle.textContent = "Swipe / scroll to compare the 3 packages. Click outside to close.";

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

  function planToHTML(p){
    const li = (p.includes || []).map(x => `<li>${escapeHtml(x)}</li>`).join("");
    return `
      <article class="plan ${p.featured ? "featured" : ""}">
        <div class="tag">${escapeHtml(p.tag || "")}</div>
        <h3>${escapeHtml(p.name)}</h3>
        <ul>${li}</ul>
        <div class="price">${escapeHtml(p.price || "")}</div>
        <div class="cta">
          <a class="btn primary" href="#contact" onclick="document.getElementById('pricingModal').classList.remove('is-open')">
            Choose this plan
          </a>
        </div>
      </article>
    `;
  }

  function escapeHtml(str){
    return String(str)
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  // Click handlers on service cards
  document.querySelectorAll(".svc-btn").forEach(btn => {
    btn.addEventListener("click", () => openModal(btn.dataset.service));
  });

  // Close modal (backdrop or close button)
  modal.addEventListener("click", (e) => {
    const close = e.target && e.target.dataset && e.target.dataset.close === "true";
    if (close) closeModal();
  });

  // ESC closes modal
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("is-open")) closeModal();
  });
});