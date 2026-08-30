// Pega Vehicle Service Management - Portal State Controller

let currentStage = 1;
let caseSequence = 2026;

const caseStatuses = {
  1: "PENDING-INTAKE",
  2: "PENDING-DIAGNOSIS",
  3: "PENDING-APPROVAL",
  4: "UNDER-REPAIR",
  5: "RESOLVED-COMPLETED"
};

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  calculateCosts();
  updateCaseSummary();
});

function setupEventListeners() {
  document.getElementById("btn-ai-fill").addEventListener("click", fillFormWithAI);
  document.getElementById("btn-new-case").addEventListener("click", resetNewCase);
  
  // Real-time input updates to left panel
  document.getElementById("inp-customer").addEventListener("change", updateCaseSummary);
  document.getElementById("inp-vehicle").addEventListener("change", updateCaseSummary);
  document.getElementById("inp-title").addEventListener("input", updateCaseSummary);
}

// Stage Navigation Controller
function goToStage(stageNum) {
  if (stageNum < 1 || stageNum > 5) return;
  
  currentStage = stageNum;

  // Update Chevrons
  for (let i = 1; i <= 5; i++) {
    const chev = document.getElementById(`chev-${i}`);
    chev.classList.remove("active", "completed");
    
    if (i < stageNum) {
      chev.classList.add("completed");
    } else if (i === stageNum) {
      chev.classList.add("active");
    }
  }

  // Update Panes
  document.querySelectorAll(".stage-pane").forEach(pane => pane.classList.remove("active"));
  const targetPane = document.getElementById(`stage-${stageNum}`);
  if (targetPane) targetPane.classList.add("active");

  // Update Case Status
  const statusLabel = caseStatuses[stageNum] || "OPEN";
  document.getElementById("display-status").innerText = statusLabel;

  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Update Invoice on final stage
  if (stageNum === 5) {
    populateInvoice();
  }
}

// Declarative Real-Time Calculation Engine
function calculateCosts() {
  const laborVal = parseFloat(document.getElementById("sel-labor").value) || 0;
  const partsVal = parseFloat(document.getElementById("sel-parts").value) || 0;

  const subtotal = laborVal + partsVal;
  const gstRate = 0.18; // 18% GST standard in India
  const tax = subtotal * gstRate;
  const grandTotal = subtotal + tax;

  // Format to INR
  document.getElementById("disp-labor").innerText = formatINR(laborVal);
  document.getElementById("disp-parts").innerText = formatINR(partsVal);
  document.getElementById("disp-subtotal").innerText = formatINR(subtotal);
  document.getElementById("disp-tax").innerText = formatINR(tax);
  document.getElementById("disp-grand").innerText = formatINR(grandTotal);

  // Update summary card
  document.getElementById("sum-cost").innerText = formatINR(grandTotal);
}

// Update Left Case Summary Card
function updateCaseSummary() {
  const custSelect = document.getElementById("inp-customer");
  const vehSelect = document.getElementById("inp-vehicle");
  const titleInput = document.getElementById("inp-title");

  const custText = custSelect.options[custSelect.selectedIndex]?.text || "Not Selected";
  const vehText = vehSelect.options[vehSelect.selectedIndex]?.text || "Not Selected";

  document.getElementById("sum-customer").innerText = custText.split("—")[0].trim() || "Not Selected";
  document.getElementById("sum-vehicle").innerText = vehText.split("(")[0].trim() || "Not Selected";
  document.getElementById("sum-title").innerText = titleInput.value || "Vehicle Service";
}

// AI Form Assistant Generator
function fillFormWithAI() {
  const aiSamples = [
    {
      customer: "vin-cus011",
      vehicle: "Creta SX",
      title: "Suspension Noise & 20,000 KM Periodic Maintenance",
      symptoms: "Rattling noise from front right suspension when driving over speed bumps. Minor squeal from disc brakes. Request engine oil change."
    },
    {
      customer: "vin-cus001",
      vehicle: "Toyota Camry",
      title: "Hybrid Battery Checkup & Brake Pad Replacement",
      symptoms: "Periodic service indicator light on. Brake pedal feels slightly soft under heavy braking. Battery diagnostic check requested."
    },
    {
      customer: "vin-cus918",
      vehicle: "MG ZS EV",
      title: "High Voltage Electrical & AC Cooling Diagnostic",
      symptoms: "AC cabin blower cooling is intermittent. Request software firmware update and tire rotation."
    }
  ];

  const randomSample = aiSamples[Math.floor(Math.random() * aiSamples.length)];

  document.getElementById("inp-customer").value = randomSample.customer;
  document.getElementById("inp-vehicle").value = randomSample.vehicle;
  document.getElementById("inp-title").value = randomSample.title;
  document.getElementById("inp-symptoms").value = randomSample.symptoms;

  updateCaseSummary();

  // Subtle button pulse
  const btn = document.getElementById("btn-ai-fill");
  btn.style.transform = "scale(0.95)";
  setTimeout(() => btn.style.transform = "scale(1)", 150);
}

// Populate Digital Invoice on Completion
function populateInvoice() {
  const custSelect = document.getElementById("inp-customer");
  const vehSelect = document.getElementById("inp-vehicle");
  const grandTotal = document.getElementById("disp-grand").innerText;

  document.getElementById("final-case-id").innerText = document.getElementById("display-case-id").innerText;
  document.getElementById("inv-cust").innerText = custSelect.options[custSelect.selectedIndex]?.text || "Customer";
  document.getElementById("inv-veh").innerText = vehSelect.options[vehSelect.selectedIndex]?.text || "Vehicle";
  document.getElementById("inv-amount").innerText = `${grandTotal} (PAID)`;
  document.getElementById("inv-date").innerText = new Date().toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  });
}

// Reset / Create Brand-New Case
function resetNewCase() {
  caseSequence += 1;
  const newCaseID = `S-${caseSequence}`;
  
  document.getElementById("display-case-id").innerText = newCaseID;
  document.getElementById("inp-customer").value = "vin-cus011";
  document.getElementById("inp-vehicle").value = "Creta SX";
  document.getElementById("inp-title").value = "Annual Periodic Maintenance & Diagnostics";
  document.getElementById("inp-symptoms").value = "Routine checkup and fluid replacement.";

  updateCaseSummary();
  calculateCosts();
  goToStage(1);
}

// Currency Formatter (INR ₹)
function formatINR(val) {
  return "₹" + Number(val).toLocaleString("en-IN", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}
