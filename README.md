# Group U BC5: Market Dashboard
 
## Group U:
- Beatriz Ferreira (20210630)
- Beatriz Peres (20210910)
- Diogo Marques (20210605)
- Miriam Hadidi (20210644)
 
## General Description
The code stored in this github repository is the source for Group U's dashboard, Market Dash. Because this dashboard is deployed via Heroku, the user does not need to install or download anything if their purpose is only to view and interact with the dashboard. However, if edits to the code are needed, the user would need to download and install PyCharm, the entire repository, and create a Heroku account to deploy once again.
The dashboard contains two pages: Asset Insights and Market Overview, as well as a link to return to the github repository. The Asset Insights page is the main landing page because one of the primary dashboard requirements was to include prediction data. It displays daily updated information regarding any cryptocurrency or stock the user wishes to view. This page focuses on looking deeper into a single asset, from key metrics to a candlestick and prediction plot.
The Market Overview page is the secondary page as it contains additional information we find will be interesting for the company and potential investors. As named, this page provides an overview of the cryptocurrency and stock market with world indices, a crypto-stock comparison, top rankings by market capitalization, bull vs bear assessment, fear vs greed index, and news articles.
 
## Instructions
First, navigate to the publicly available dashboard: https://cryptodash-groupu.herokuapp.com/
 
### Asset Insights
1) The user can type in and select one of 18,592 ticker symbols or asset names which will update all KPIs and plots on this page.
2) The user can also choose one of five pre-set timeframes (last 5 days, last month, last 6 months, last year, or full*).
Note: This and the first step can be switched around as the menu options will retain the user's selection.
*The Full timeframe is based on the start date of the particular asset chosen.
 
Selecting various coins and timeframes will update the entire page's visualizations:
- KPIs
  - Current price
  - Last day change (in both USD and percentage)
  - Highest price within chosen time period
  - Lowest price within chosen time period
  - Relative Strength Index (current)
- Visualizations
  - Price Analysis: a candlestick plot with the simple moving averages (SMA50 and SMA100)
  - Historical time series with the prediction appended to make one complete plot
  - Table containing the predicted prices of the given crypto for the following ten days
 
### Market Overview
Use the sidebar on the left-hand side of the page to navigate to the market overview.
Most visualizations on this page are for observational purposes and update daily along with the rest of the data. As this page does not contain any callbacks,  the instructions are more to walk the user through descriptive aspects. The visualizations are listed and explained below.

1) World Stock Indices Trending: The user can see some of the top stock indices from around the world:
- North America: S&P 500 in USD
- Europe: FTSE 100 in GBP
- South America: IBOVESPA in BRL
- Asia: SSE Composite in CNY
The line plot represents a trending view of the past year of the particular index accompanied by the last price and day change.

2) Next, the user can see the returns of a cryptocurrency portfolio (using the CMC Crypto 200 index) in comparison to a stock portfolio (using the S&P 500 index). The “simulation” imagines that the user invested $1000 one year ago.

3) One can then view the top 10 cryptocurrencies by market capitalization, along with these same currencies showing a bear or bull trend.

4) Finally, we display the daily calculated Fear vs Greed Index on a gauge with red indicating extreme fear and green indicating extreme greed in the cryptocurrency market.

5) Next to this, we continue the theme and look at general market sentiment through news articles. Links are provided for each article so the user can read more as they wish.

## Screenshots
### Asset Insights
![image](https://user-images.githubusercontent.com/90759275/171040019-2d2a36a6-0d05-418a-b63a-86a295bbed2f.png)
![image](https://user-images.githubusercontent.com/90759275/171040080-b8f5ff56-4fab-42f9-88d4-b5968f14ec2b.png)
![image](https://user-images.githubusercontent.com/90759275/171040113-7fca44bf-9f5c-4f0a-bdec-a80812ae3758.png)

### Market Overview
![image](https://user-images.githubusercontent.com/90759275/171040269-8b25d40b-5f8f-4d57-9893-db65d8ae28e8.png)
![image](https://user-images.githubusercontent.com/90759275/171040301-35018b3b-586d-498e-9abb-dfe55b170b66.png)
![image](https://user-images.githubusercontent.com/90759275/171040328-a1f39574-25d3-4670-8d2f-8b5173a66bc9.png)
![image](https://user-images.githubusercontent.com/90759275/171040358-d405bdd6-1067-49ca-b298-5a97d3750d39.png)
![image](https://user-images.githubusercontent.com/90759275/171040378-0b7dc159-8743-42e1-a169-3ef6700823cc.png)

