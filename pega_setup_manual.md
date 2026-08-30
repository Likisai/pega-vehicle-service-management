# Vehicle Service Management — Setup & Configuration Manual
### 🛠️ Pega Infinity & Blueprint Deployment Guide

This guide walks through the exact setup used to deploy and configure the **Vehicle Service Management** application inside Pega Infinity 24.1 / 8.8.

---

## 🏗️ 1. Architecture Overview & Case Lifecycle

The primary case type is **`Submit Vehicle Service Request`** (`Prefix: S-`), structured into 5 distinct stages:

1. **Request Intake:** Customer search & selection (`vin-cus011`), vehicle allocation, and symptom logging.
2. **Inspection Diagnosis:** Multi-point safety checklist and technician diagnostic notes (`tech1@vehicle.com`).
3. **Estimate Approval:** Itemized labor and parts selection with auto-calculating GST taxes and totals.
4. **Service Execution:** Warehouse part dispatch, technician execution, and senior advisor quality sign-off.
5. **Service Completion:** Digital receipt generation, audit logging, and case resolution (`Resolved-Completed`).

---

## 📥 2. Blueprint Import into Pega

1. Open your Pega Dev Studio / App Studio environment.
2. In the top-left application menu, select **New Application**.
3. Choose **Build from Pega Blueprint**.
4. Upload `Vehicle_Service_Management.blueprint` from this repository.
5. Pega will scaffold all 5 stages, standard data objects (`Customer`, `Vehicle`, `Service Estimate`, `Vehicle Inspection Report`), and user roles.

---

## ⚙️ 3. Key Configuration Fixes (Pega Best Practices)

### A. External Database Mapping (`.pyLabel` fix)
When using external database tables without a blob column, standard Pega autocompletes default to querying `.pyLabel`.
* In Dev Studio, open the **`UPlus-VehicleS-Data-Customer`** Class rule.
* Navigate to the **External Mapping** tab.
* Map property **`.pyLabel`** (Case sensitive) to database column **`customerlabel`**.
* Open the Database Table rule and click **Test Connection** to flush the schema cache.

### B. Utility vs. User Step Configuration
* For manual technician inputs (e.g. *Log Findings*), configure the step as a **`Collect Information`** step (green icon) rather than an automation/utility step to avoid `UnresolvedAssemblyError`.

### C. Declarative Pricing Calculations
* Configure the calculation expressions on the Case Data Model (`Subtotal = LaborServicesTotal + ReplacementPartsTotal`, `GrandTotal = Subtotal + TaxAmount`).

---

## 🚀 4. Running the Demo Portal

You can test the frontend workflow immediately in your browser by opening `index.html` or visiting the live GitHub Pages link.
