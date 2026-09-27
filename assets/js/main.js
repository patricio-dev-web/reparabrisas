"use strict";

const menuButton = document.querySelector(".menu-toggle");
const navLinks = document.querySelector("#nav-links");
if (menuButton && navLinks) {
  menuButton.hidden = false;
  navLinks.dataset.enhanced = "true";
  const setMenu = (open, restoreFocus = false) => {
    navLinks.classList.toggle("is-open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    if (restoreFocus) menuButton.focus();
  };
  setMenu(false);
  menuButton.addEventListener("click", () => setMenu(menuButton.getAttribute("aria-expanded") !== "true"));
  navLinks.addEventListener("click", (event) => { if (event.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", (event) => { if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") setMenu(false, true); });
  document.addEventListener("click", (event) => { if (!event.target.closest(".nav")) setMenu(false); });
  window.matchMedia("(min-width: 961px)").addEventListener("change", () => setMenu(false));
}

// Hook local, sin proveedor de analítica ni envío de datos personales.
// Conectar a un proveedor sólo al configurar su cuenta y política de privacidad.
function trackContact(source) {
  document.dispatchEvent(new CustomEvent("reparabrisas:contact", { detail: { source } }));
}
document.querySelectorAll("[data-contact]").forEach((link) => {
  link.addEventListener("click", () => trackContact(link.dataset.contact));
});

const quoteForm = document.querySelector("#quote-form");
if (quoteForm) {
  quoteForm.querySelector('button[type="submit"]').hidden = false;
  quoteForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const commune = quoteForm.elements.commune.value.trim();
    if (!commune) { quoteForm.elements.commune.setCustomValidity("Escribe tu comuna."); quoteForm.elements.commune.reportValidity(); return; }
    const vehicle = quoteForm.elements.vehicle.value.trim();
    const message = `Hola, quiero cotizar: ${quoteForm.elements.service.value}.\nMi comuna es: ${commune}.${vehicle ? `\nMi vehículo es: ${vehicle}.` : ""}\nMe gustaría confirmar disponibilidad, precio y condiciones del servicio.`;
    trackContact("quote-form");
    window.location.assign(`https://wa.me/56976957866?text=${encodeURIComponent(message)}`);
  });
  quoteForm.elements.commune.addEventListener("input", () => quoteForm.elements.commune.setCustomValidity(""));
}

document.querySelectorAll("[data-video-id]").forEach((shell) => {
  const button = shell.querySelector(".video-trigger");
  if (!button) return;
  button.hidden = false;
  button.addEventListener("click", () => {
    const id = shell.dataset.videoId;
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
    const iframe = document.createElement("iframe");
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1`;
    iframe.title = "Video de demostración de YouTube; no corresponde a un servicio realizado";
    iframe.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    shell.replaceChildren(iframe);
    iframe.focus();
  }, { once: true });
});
document.querySelectorAll("[data-year]").forEach((element) => { element.textContent = new Date().getFullYear(); });
