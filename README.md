# Smart Customer Segmentation Engine

An end-to-end Machine Learning and Data Engineering pipeline that transforms raw retail transaction data into actionable business intelligence using **RFM Analysis** and **K-Means Clustering**.

## 🚀 The Real-World Problem
Retail businesses waste resources sending generic marketing to their entire customer base. This engine solves that by processing thousands of transactions through a local SQL data warehouse, engineering Recency, Frequency, and Monetary (RFM) features, and using Unsupervised Machine Learning to automatically group customers into profitable segments (e.g., "VIPs" and "At Risk/Churning").

## ⚠️ Important Note on Data Files
Due to GitHub's file size limits, the raw dataset (`online_retail.csv`) and the populated SQLite databases (`retail_real.db`) are not hosted in this repository. 

**To run this project locally:**
1. Download the data and database files from my Google Drive: [INSERT_YOUR_GOOGLE_DRIVE_LINK_HERE]
2. Paste the downloaded `.csv` and `.db` files directly into the root folder of this repository.

## 🛠️ Tech Stack
* **Database:** SQLite, Advanced SQL (CTEs, Window Functions, Cross Joins)
* **Data Manipulation:** Python, Pandas
* **Machine Learning:** Scikit-Learn (K-Means, StandardScaler)
* **Visualization:** Plotly (Interactive 3D Scatter Plots)

## 🏗️ Pipeline Architecture

1. **Data Ingestion & Warehousing (Step 1):** Automated ingestion of raw CSV data into a local SQLite database, handling missing values and the "Guest Checkout" problem.
2. **Feature Engineering (Step 2):** Advanced SQL queries utilizing Common Table Expressions (CTEs) to dynamically calculate RFM values based on the maximum transaction date in the warehouse.
3. **Machine Learning Model (Step 3):** Data scaling and K-Means clustering. Optimized the number of clusters (K=3) using the mathematical Elbow Method to minimize Within-Cluster Sum of Squares (WCSS).
4. **Deployment & Visualization (Step 4):** Generated an interactive 3D Plotly visualization for data storytelling and deployed the mathematical cluster labels back into a new `customer_segments` SQL table for CRM integration.

## 📊 Business Strategy Outcomes
The algorithm successfully segmented the customer base into three distinct archetypes:
* **Cluster 0 (VIPs):** High spend, high frequency, recent purchases. *Strategy: Protect margins, offer exclusive early access instead of discounts.*
* **Cluster 1 (At Risk / Churning):** Low spend, low frequency, hasn't purchased in months. *Strategy: Aggressive win-back discounts; remove from paid ad targeting if unresponsive.*
* **Cluster 2 (Recent Regulars):** Average spend, active recently. *Strategy: Algorithmic cross-selling and loyalty program nudges to graduate them to VIP status.*

## 💻 How to Run
1. Clone the repository: `git clone [YOUR_REPO_URL]`
2. Download the data from the Google Drive link above and place it in the root folder.
3. Install the required dependencies:
   ```bash
   pip install pandas scikit-learn plotly
