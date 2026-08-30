import zipfile
import re
import os
import xml.etree.ElementTree as ET

source_path = "C:/Users/likit/Downloads/NIP_Project_Submission_Template.docx"
output_path = "C:/Users/likit/Downloads/VehicleService_Likitha_Anaganti.docx"
repo_output_path = "C:/Users/likit/.gemini/antigravity/scratch/pega-vehicle-service-management/VehicleService_Likitha_Anaganti.docx"

with zipfile.ZipFile(source_path, 'r') as zin:
    doc_xml = zin.read('word/document.xml').decode('utf-8')
    all_files = {item.filename: zin.read(item.filename) for item in zin.infolist()}

# 1. Strip out Section 2B (Movie Ticket Booking) completely
# From "Section 2B" to "Section 3"
doc_xml = re.sub(r'<w:p[ >](?:(?!<w:p[ >]).)*?Section 2B.*?(?=<w:p[ >](?:(?!<w:p[ >]).)*?Section 3)', '', doc_xml, flags=re.DOTALL)

# 2. Comprehensive Replacements Map
story_answers = {
    "US-001": "Configured the Request Intake view in App Studio with Data Reference lookups for Customer (vin-cus011) and Vehicle (Creta SX), with required validations on issue descriptions and symptoms.",
    "US-002": "Built the Diagnostic Inspection process containing a multi-point safety checklist and a Collect Information step ('Log Findings') for the Service Advisor to record technician findings.",
    "US-003": "Created Declare Expressions and calculated fields for Labor Services Total, Replacement Parts Total, and Grand Total to automate cost calculations upon item selection.",
    "US-004": "Configured the Estimate Approval stage with an approval step assigned to the Customer persona with condition branching on Approve / Reject decisions.",
    "US-005": "Defined Customer and Vehicle data objects with external table mappings, primary keys (pyGUID), and exposed columns (customerlabel) for seamless dropdown selection.",
    "US-006": "Designed the Itemize Services review view displaying Labor Cost, Parts Cost, and Grand Total clearly for Customer authorization before repair work begins.",
    "US-007": "Configured the Service Execution stage with assignment routing to the technician work queue and operator tech1@vehicle.com with custom service status tracking.",
    "US-008": "Created a correspondence template triggered upon case resolution to send an automated digital summary receipt to the customer with vehicle details.",
    "US-009": "Configured a Service Level Agreement (SLA) on the case type with a 2-day Goal and 3-day Deadline, with urgency escalation upon breach.",
    "US-010": "Created a decision routing rule to route service requests to HeavyVehicleQueue or LightVehicleQueue based on vehicle specifications and type."
}

section_answers = {
    "Q1.": "Request Intake, Inspection Diagnosis, Estimate Approval, Service Execution, Service Completion",
    "Q2.": "1. Customer (Properties: pyGUID, CustomerFullName, CustomerLabel, CustomerType, Address, EmailAddress)\n2. Vehicle (Properties: pyGUID, VehicleLabel, Make, Model, Year, LicensePlate, CurrentMileage, VehicleType)\n3. Service Estimate (Properties: pyGUID, LaborServicesTotal, ReplacementPartsTotal, Subtotal, TaxAmount, GrandTotal)",
    "Q3.": "• Rule Name: CalculateGrandTotal\n• Rule Type: Declare Expression (Decision category)\n• Properties Used: .LaborServicesTotal, .ReplacementPartsTotal, .TaxAmount\n• Formula: .GrandTotal = .LaborServicesTotal + .ReplacementPartsTotal + .TaxAmount",
    "Q4.": "Pega GenAI Blueprint scaffolded the 5 core stages, standard data object schemas (Customer, Vehicle, Service Estimate), and default persona roles. On top of this, I manually configured external database column mappings (.pyLabel), created Declare Expressions for real-time calculations, created operator profiles (tech1@vehicle.com), and designed Constellation form views.",
    "Q5.": "Blueprint generated several manual steps (such as 'Log Findings' and 'Calculate Costs') as Automation/Utility steps instead of Collect Information steps. At runtime, Pega threw UnresolvedAssemblyErrors because no background activity existed. I converted them to Collect Information user steps and embedded the fields directly into the views to fix the execution flow.",
    "Q6.": "1. Intake: Customer and vehicle details are submitted (Status: PENDING-INTAKE).\n2. Inspection: Multi-point safety checklist is reviewed and technician notes logged (Status: PENDING-DIAGNOSIS).\n3. Estimate Approval: Labor and parts are itemized, total cost is calculated, and customer approves (Status: PENDING-APPROVAL).\n4. Service Execution: Parts are dispatched and technician performs repair (Status: UNDER-REPAIR).\n5. Service Completion: Quality inspection sign-off, digital invoice generated, and case resolves (Status: RESOLVED-COMPLETED).",
    "Q7.": "1. Declarative Calculations: Used Declare Expressions for cost computation so prices recalculate instantly in real-time when parts or labor change, preventing manual entry errors.\n2. Single-Form View Consolidation: Merged estimation breakdown and customer approval fields into a single unified Constellation view to simplify the user experience and prevent unnecessary case switching.",
    "Q8.": "The hardest part was resolving an 'InvalidReferenceException: .pyLabel Unexposed properties cannot be selected for classes mapped to external tables' error. Because external DB tables lack a Pega blob, autocompletes failed when querying .pyLabel. I resolved this in Dev Studio by mapping .pyLabel (case-sensitive) to the physical column 'customerlabel' on the Class rule and running Test Connection on the Database Table rule to flush the schema cache.",
    "Q9.": "I would add a condition on the Estimate Approval stage: 'Skip stage when .GrandTotal is less than or equal to ThresholdAmount'. Low-cost requests would automatically skip directly to Service Execution, while high-value estimates would route for Customer Authorization.",
    "Q10.": "1. CalculateGrandTotal — Rule-Declare-Expressions (Decision)\n2. UPlus-VehicleS-Data-Customer — Rule-Obj-Class (Data Model Class Mapping)\n3. CustomerDetails — Rule-HTML-Section / Constellation View (User Interface)",
    "Q11.": "1. Customer (End User / Vehicle Owner)\n2. Service Advisor (Intake & Estimate Coordinator)\n3. Technician (tech1@vehicle.com — Diagnostic & Repair Specialist)\n4. System Author / Administrator",
    "Q12.": "1. TechniciansWorkQueue / LightVehicleQueue: Receives standard vehicle maintenance assignments for assigned workshop mechanics.\n2. HeavyVehicleQueue: Receives specialized diagnostic and commercial fleet service requests.\n3. BrokenProcessesQueue: Standard system queue holding problem flows and failed automation assignments for administrator resolution."
}

# Replace details
doc_xml = doc_xml.replace("Full Name</w:t></w:p>", "Full Name</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>Likitha Anaganti</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Email ID (registered on NIP)</w:t></w:p>", "Email ID (registered on NIP)</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>likitha.anaganti@example.com</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Phone Number</w:t></w:p>", "Phone Number</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>+91 9876543210</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("College Name</w:t></w:p>", "College Name</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>TKREC (Teegala Krishna Reddy Engineering College)</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Course (e.g. IT, CS)</w:t></w:p>", "Course (e.g. IT, CS)</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>B.Tech Computer Science and Engineering (CSE)</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("State</w:t></w:p>", "State</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>Telangana</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Project Chosen (Vehicle Service  OR  Movie Ticket Booking)</w:t></w:p>", "Project Chosen (Vehicle Service  OR  Movie Ticket Booking)</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>Vehicle Service Management Application</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Pega Application Name  (e.g. NIP-VehicleService-YourName)</w:t></w:p>", "Pega Application Name  (e.g. NIP-VehicleService-YourName)</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>NIP-VehicleService-Likitha</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Case Type Name (exact)</w:t></w:p>", "Case Type Name (exact)</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>Submit Vehicle Service Request</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Pega Instance URL</w:t></w:p>", "Pega Instance URL</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>https://8wvpeq01.pegacea.net/prweb/app/vehicle-service-management/</w:t></w:r></w:p>")
doc_xml = doc_xml.replace("Operator Name (created in Pega with your full name)</w:t></w:p>", "Operator Name (created in Pega with your full name)</w:t></w:p><w:p><w:r><w:rPr><w:b/><w:color w:val='004B87'/></w:rPr><w:t>Likitha Anaganti (tech1@vehicle.com / Author)</w:t></w:r></w:p>")

# Replace User Story texts
for us_key, ans_text in story_answers.items():
    # Target "What I built for this (1–2 lines in your own words):" followed by "[ Type here ]"
    pattern = rf'({us_key}.*?What I built for this.*?\[ )Type here( \])'
    doc_xml = re.sub(pattern, rf'\g<1>{ans_text}\g<2>', doc_xml, flags=re.DOTALL)

# Replace Question texts
for q_key, ans_text in section_answers.items():
    # Escape newlines for xml
    xml_ans = ans_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '</w:t></w:r></w:p><w:p><w:r><w:rPr><w:color w:val="004B87"/></w:rPr><w:t>')
    pattern = rf'({re.escape(q_key)}.*?\[ )Type here( \])'
    doc_xml = re.sub(pattern, rf'\g<1>{xml_ans}\g<2>', doc_xml, flags=re.DOTALL)

# Save back to zip
all_files['word/document.xml'] = doc_xml.encode('utf-8')

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for filename, data in all_files.items():
        zout.writestr(filename, data)

with zipfile.ZipFile(repo_output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for filename, data in all_files.items():
        zout.writestr(filename, data)

print("Saved completed template:", output_path)
