// Verifica el mensaje y la validación sin abrir WhatsApp ni enviar mensajes.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const events = {};
const telemetry = [];
let navigation = null;
let invalidMessage = "";
let validityReported = false;
const commune = {
  value: "  Quilicura  ",
  setCustomValidity(message) { invalidMessage = message; },
  reportValidity() { validityReported = true; },
  addEventListener(type, callback) { events[`commune:${type}`] = callback; },
};
const form = {
  elements: { commune, service: { value: "Reparación de parabrisas" }, vehicle: { value: "Citroën C3 & C4" } },
  querySelector() { return { hidden: true }; },
  addEventListener(type, callback) { events[type] = callback; },
};
const sandbox = {
  document: {
    querySelector(selector) { return selector === "#quote-form" ? form : null; },
    querySelectorAll() { return []; },
    dispatchEvent(event) { telemetry.push(event.detail); },
  },
  window: { location: { assign(url) { navigation = url; } } },
  CustomEvent: class { constructor(type, options) { this.type = type; this.detail = options.detail; } },
};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, "../assets/js/main.js"), "utf8"), sandbox);
let prevented = false;
events.submit({ preventDefault() { prevented = true; } });
assert.ok(prevented);
const url = new URL(navigation);
assert.equal(url.origin + url.pathname, "https://wa.me/56976957866");
assert.match(url.searchParams.get("text"), /Mi comuna es: Quilicura\./);
assert.match(url.searchParams.get("text"), /Citroën C3 & C4/);
assert.deepEqual(Object.keys(telemetry[0]), ["source"]);
assert.equal(telemetry[0].source, "quote-form");
commune.value = "   ";
navigation = null;
events.submit({ preventDefault() {} });
assert.equal(navigation, null);
assert.ok(validityReported && invalidMessage);
commune.value = "Colina";
events["commune:input"]();
assert.equal(invalidMessage, "");
form.elements.vehicle.value = "";
events.submit({ preventDefault() {} });
assert.ok(!new URL(navigation).searchParams.get("text").includes("Mi vehículo"));
console.log("OK: número, mensaje con acentos, validación, campo opcional y evento sin datos personales.");
