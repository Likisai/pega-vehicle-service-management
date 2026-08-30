import zipfile
import os

def create_docx(filename="Vehicle_Service_Management_Report.docx"):
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="22"/>
        <w:color w:val="333333"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="004B87"/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="1E5CB3"/><w:sz w:val="26"/></w:rPr>
  </w:style>
</w:styles>"""

    document = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="200"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:color w:val="004B87"/>
          <w:sz w:val="48"/>
        </w:rPr>
        <w:t>Vehicle Service Management System</w:t>
      </w:r>
    </w:p>
    
    <w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:after="400"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:i/>
          <w:color w:val="555555"/>
          <w:sz w:val="26"/>
        </w:rPr>
        <w:t>Pega Infinity 24.1 / 8.8 — Capstone Project &amp; Technical Report</w:t>
      </w:r>
    </w:p>

    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>1. Executive Summary</w:t></w:r></w:p>
    <w:p><w:r><w:t>The Vehicle Service Management System is an enterprise-grade solution built using the Pega Infinity Low-Code Platform and Pega GenAI Blueprint. It streamlines the automotive repair lifecycle, replacing disparate manual service tracking with an automated, end-to-end Case Management architecture.</w:t></w:r></w:p>

    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>2. Case Lifecycle Architecture</w:t></w:r></w:p>
    <w:p><w:r><w:t>The primary case type 'Submit Vehicle Service Request' (Case Prefix: S-) is organized into five sequential stages:</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Stage 1 (Request Intake): Customer profile resolution (vin-cus011), vehicle data mapping, and symptom logging.</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Stage 2 (Inspection Diagnosis): Multi-point technical checklist review and diagnosis notes recording.</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Stage 3 (Estimate Approval): Dynamic cost itemization of labor and replacement parts with auto-calculating GST (18%).</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Stage 4 (Service Execution): Parts fulfillment, technician allocation (tech1@vehicle.com), and quality inspection.</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Stage 5 (Service Completion): Final digital invoice generation, customer notification, and case resolution.</w:t></w:r></w:p>

    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>3. Data Model &amp; Key Technical Solutions</w:t></w:r></w:p>
    <w:p><w:r><w:t>• External Database Mapping: Resolved the .pyLabel unexposed database exception on external tables by mapping .pyLabel to the physical column 'customerlabel' and refreshing the DB connection cache.</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Declarative Cost Calculations: Built automated Declare Expressions for Labor Services Total, Replacement Parts Total, Subtotal, GST, and Grand Total.</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Operator &amp; Work Queue Routing: Configured the Technician persona (tech1@vehicle.com) under the VehicleS:Authors access group.</w:t></w:r></w:p>

    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>4. Live Demo &amp; Repository</w:t></w:r></w:p>
    <w:p><w:r><w:t>• Live Demo Portal: https://likisai.github.io/pega-vehicle-service-management/</w:t></w:r></w:p>
    <w:p><w:r><w:t>• GitHub Repository: https://github.com/Likisai/pega-vehicle-service-management</w:t></w:r></w:p>
    
    <w:sectPr/>
  </w:body>
</w:document>"""

    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', content_types)
        docx.writestr('_rels/.rels', rels)
        docx.writestr('word/_rels/document.xml.rels', doc_rels)
        docx.writestr('word/document.xml', document)
        docx.writestr('word/styles.xml', styles)
    
    print(f"Created {filename} successfully using pure Python standard library!")

if __name__ == "__main__":
    create_docx("Vehicle_Service_Management_Report.docx")
