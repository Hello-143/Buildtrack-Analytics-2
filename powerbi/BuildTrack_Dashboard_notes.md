# BuildTrack Analytics: Power BI Specification

This specification document outlines data load transformations, schema configurations, DAX measures, and page-by-page wireframe layouts to build the dashboard in **Power BI Desktop**.

---

## 1. Power Query M-Code Steps

### A. Dim_Projects Query
```powerquery
let
    Source = Csv.Document(File.Contents("E:\Projects\buildtrack-analytics\data\processed\projects_clean.csv"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"project_id", Int64.Type}, {"project_name", type text}, {"project_type", type text}, {"start_date", type date}, {"planned_end_date", type date}, {"actual_end_date", type date}, {"budgeted_cost", type number}, {"actual_cost", type number}, {"status", type text}})
in
    #"Changed Type"
```

### B. Fact_Material_Vendor Query
```powerquery
let
    Source = Csv.Document(File.Contents("E:\Projects\buildtrack-analytics\data\processed\material_vendor_clean.csv"),[Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"record_id", Int64.Type}, {"project_id", Int64.Type}, {"material_type", type text}, {"vendor_name", type text}, {"ordered_qty", type number}, {"delivered_qty", type number}, {"wastage_pct", type number}, {"promised_delivery_date", type date}, {"actual_delivery_date", type date}, {"on_time", Int64.Type}})
in
    #"Changed Type"
```

### C. Fact_Labour_Attendance Query
```powerquery
let
    Source = Csv.Document(File.Contents("E:\Projects\buildtrack-analytics\data\processed\labour_attendance_clean.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"record_id", Int64.Type}, {"project_id", Int64.Type}, {"site_name", type text}, {"date", type date}, {"workers_expected", Int64.Type}, {"workers_present", Int64.Type}, {"attendance_pct", type number}})
in
    #"Changed Type"
```

### D. Fact_Risk_Flags Query
```powerquery
let
    Source = Csv.Document(File.Contents("E:\Projects\buildtrack-analytics\reports\risk_flags.csv"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"project_id", Int64.Type}, {"project_name", type text}, {"project_type", type text}, {"status", type text}, {"predicted_risk_label", type text}})
in
    #"Changed Type"
```

---

## 2. Model Schema Configuration

In the **Model View**, build the relationships:
* `Dim_Projects[project_id]` (1) $\rightarrow$ `Fact_Material_Vendor[project_id]` ($\infty$) [Single filtering]
* `Dim_Projects[project_id]` (1) $\rightarrow$ `Fact_Labour_Attendance[project_id]` ($\infty$) [Single filtering]
* `Dim_Projects[project_id]` (1) $\leftrightarrow$ `Fact_Risk_Flags[project_id]` (1) [Bi-directional or 1-to-1]

---

## 3. Comprehensive DAX Measures List

### Measure 1: Total Budgeted Cost
```dax
Total Budget = SUM(projects[budgeted_cost])
```
*Format: Currency, 0 decimal places.*

### Measure 2: Total Actual Cost
```dax
Total Actual = SUM(projects[actual_cost])
```
*Format: Currency, 0 decimal places.*

### Measure 3: Cost Variance %
```dax
Cost Variance % = DIVIDE([Total Actual] - [Total Budget], [Total Budget])
```
*Format: Percentage (`0.0%`).*

### Measure 4: Total Projects Count
```dax
Total Projects = COUNTROWS(projects)
```

### Measure 5: Delayed Projects Count
```dax
Delayed Projects Count = CALCULATE(COUNT(projects[project_id]), projects[status] = "Delayed")
```

### Measure 6: Average Attendance %
```dax
Average Attendance % = AVERAGE(labour_attendance[attendance_pct]) / 100
```
*Format: Percentage (`0.0%`).*

### Measure 7: Expected Man-Days
```dax
Expected Man-Days = SUM(labour_attendance[workers_expected])
```

### Measure 8: Present Man-Days
```dax
Present Man-Days = SUM(labour_attendance[workers_present])
```

### Measure 9: Average Wastage %
```dax
Average Wastage % = AVERAGE(material_vendor[wastage_pct]) / 100
```
*Format: Percentage (`0.1%`).*

### Measure 10: On-Time Delivery Rate %
```dax
On-Time Delivery Rate % = DIVIDE(CALCULATE(COUNT(material_vendor[record_id]), material_vendor[on_time] = 1), COUNT(material_vendor[record_id]))
```
*Format: Percentage (`0.0%`).*

### Measure 11: Quantity Fulfillment Rate %
```dax
Quantity Fulfillment Rate % = DIVIDE(SUM(material_vendor[delivered_qty]), SUM(material_vendor[ordered_qty]))
```
*Format: Percentage (`0.0%`).*

### Measure 12: High-Risk Projects Count
```dax
High-Risk Projects Count = CALCULATE(COUNT(Fact_Risk_Flags[project_id]), Fact_Risk_Flags[predicted_risk_label] = "High")
```

---

## 4. Dashboard Page Wireframes

### Page 1: Executive Summary
Designed for branch heads to monitor high-level metrics and active risks at a glance.

```
+------------------------------------------------------------------------------------+
|  Gupta Engineers & Contractors - Executive Dashboard             [Division Filter] |
+------------------------------------------------------------------------------------+
|  [Total Budget]      [Total Actual]      [Cost Variance %]     [High-Risk Projects]|
|   INR 94.27M          INR 84.14M          -10.75%               6 Projects         |
+------------------------------------------------------------------------------------+
|                                         |                                          |
|  [Active Risk Alert Table]              | [Cost Variance Trend by Division]        |
|  Project Name     Risk Level  Type      |  Fabrication: +12.84%                    |
|  Proj 10          High        Fab       |  Residential: +8.90%                     |
|  Proj 18          High        Res       |  Building:    +2.36%                     |
|  Proj 22          High        Fab       |                                          |
|  Proj 29          High        Res       |                                          |
|                                         |                                          |
+------------------------------------------------------------------------------------+
|  [Top Features Driving Risk (ML Output)]                                           |
|  1. Planned Duration (42.8%) | 2. Labour Attendance (40.5%) | 3. Wastage % (16.6%)  |
+------------------------------------------------------------------------------------+
```

### Page 2: Project Overview
Detailed timelines and cost breakdowns by project type.

```
+------------------------------------------------------------------------------------+
|  Project Cost & Timeline Controls               [Status Filter]   [Division Filter]|
+------------------------------------------------------------------------------------+
|  [Total Projects]       [Average Delay]      [Overrun Projects]                    |
|   35 Projects            14.2 Days            12 Projects                          |
+------------------------------------------------------------------------------------+
|                                                                                    |
|  [Budget vs. Actual Cost Comparison by Project Name] (Column Chart)               |
|   Cost |                                                                           |
|   (M)  |   __    __          __    __          __    __                            |
|        |  |  |  |  |        |  |  |  |        |  |  |  |                           |
|        |  |B |  |A |        |B |  |A |        |B |  |A |                           |
|        |__|__|__|__|________|__|__|__|________|__|__|__|________________________   |
|               Proj 1             Proj 2             Proj 3                         |
+------------------------------------------------------------------------------------+
|  [Delay Days Distribution by Division]        | [Cost vs. Timeline Correlation]    |
|   Fabrication:   19.5 Days                    |  Scatter plot showing positive     |
|   Residential:   12.1 Days                    |  correlation between delays and    |
|   Building Cont: 6.4 Days                     |  cost overrun rates.               |
+------------------------------------------------------------------------------------+
```

### Page 3: Material & Vendor Performance
Identifies vendor reliability and pinpoint areas of waste.

```
+------------------------------------------------------------------------------------+
|  Material Wastage & Vendor Scorecard           [Material Slicer]   [Vendor Slicer] |
+------------------------------------------------------------------------------------+
|  [On-Time Delivery Rate]     [Avg Material Wastage]     [Qty Fulfillment Rate]     |
|   10.73%                      10.42%                     98.54%                    |
+------------------------------------------------------------------------------------+
|                                                                                    |
|  [Vendor Scorecard Grid: Wastage % vs. On-Time Rate] (Scatter Plot)                |
|   Wastage % |                                                                      |
|     14%     |  * Local Vendor Noida (Wastage: 13.2%, On-time: 5.9%)                |
|             |  * Local Vendor Cement (Wastage: 13.7%, On-time: 0.0%)               |
|      8%     |                      * Tata Steel (Wastage: 7.9%, On-time: 26.3%)    |
|             |____________________________________________________________________  |
|             0%                                                     30% On-Time %   |
+------------------------------------------------------------------------------------+
|  [Top Wastage Materials]                      | [Fulfillment Rate by Vendor]       |
|  1. Cement: 10.74%                            |  National: 99.5%                   |
|  2. Steel:  9.67%                             |  Local Noida: 97.4%                |
+------------------------------------------------------------------------------------+
```

### Page 4: Labour & Attendance Analytics
Site-level attendance tracking and labour shortfalls.

```
+------------------------------------------------------------------------------------+
|  Labour Attendance Dashboard                   [Site Slicer]        [Date Slider]  |
+------------------------------------------------------------------------------------+
|  [Average Attendance]      [Total Expected Mandays]      [Total Present Mandays]   |
|   82.88%                    93,124                        77,181                   |
+------------------------------------------------------------------------------------+
|                                                                                    |
|  [Daily Attendance Rate Trend Line by Site] (Line Chart)                           |
|   Att %|                                                                           |
|   100% |  ---------------------[Sec 62]------------------------------------------  |
|    80% |  ~~~~~~~~~~~~~~~~~~~~~[Sec 150 - Low Attendance Site]~~~~~~~~~~~~~~~~~~~  |
|        |_________________________________________________________________________  |
|         Jan 2025                       Mar 2025                        Jun 2025    |
+------------------------------------------------------------------------------------+
|  [Expected vs. Present Workers by Site]       | [Attendance vs. Delay Scatter]     |
|  * Sec 62:   24,500 expected / 22,100 present |  Visualizes that sites with        |
|  * Sec 150:  21,000 expected / 16,500 present |  attendance < 80% face longer      |
|  * Sec 120:  25,200 expected / 21,300 present |  timeline overruns.                |
+------------------------------------------------------------------------------------+
```
