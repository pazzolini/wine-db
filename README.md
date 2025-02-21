# Wine Database API

## Overview
This project is part of the **Database Systems (CC2005)** course. It involves designing, implementing, and querying a **relational database for wine data**, including user reviews and wine characteristics. Additionally, a **Python API** was developed to interact with the database, allowing users to retrieve detailed wine-related information via endpoints.

## Features
- **Relational database design** following the **UML model**.
- **SQL schema** for table creation and population.
- **Data import and cleaning** from CSV files.
- **RESTful API** to query wines, wineries, users, and ratings.
- Advanced SQL queries to extract insights from the data.

## Database Implementation
### 1. Adjustments to the Data Model
- **Revised UML model**: Added explicit tables for **Type, Body, and Acidity**, instead of using them as attributes of the Wine table.
- **Refined relational model**: Removed attributes that acted as foreign keys, making SQL queries more efficient.
- **Dynamic calculation of user reviews**: Eliminated redundant columns such as `NumReviews/NumRatings` from the User table, as these can be computed using SQL queries.

### 2. Table Population
#### **Database Creation**
To initialize the database schema:
```bash
sqlite3 BaseDados.db
.read caminho.sql
```
#### **Data Import**
The data was sourced from:
- `Xwines_Slim_1K_Wines.csv`
- `Xwines_Slim_150K_Ratings.csv`
- Additional CSV files for each table (cleaned and structured appropriately).

Example import command:
```bash
sqlite3 BaseDados.db
.mode csv
.import WineType.csv WineType
```
#### **Number of Entries per Table**
| Table Name   | Number of Entries |
|-------------|-----------------|
| WineType    | 6               |
| WineBody    | 5               |
| WineAcidity | 3               |
| Region      | 324             |
| Winery      | 792             |
| WineryRegion | 846            |
| Wine        | 1007            |
| User        | 10,561          |
| Rating      | 150,000         |

## Python API Implementation
A **Flask-based API** was developed to interact with the database.

### **Endpoints Overview**
| Endpoint | Functionality |
|----------|--------------|
| `/` | Displays general database statistics and links to other endpoints. |
| `/wines` | Lists all wines. |
| `/wines/<int:id>/` | Retrieves details of a specific wine. |
| `/winetypes` | Lists all wine types. |
| `/winetypes/<int:id>/` | Retrieves details of a specific wine type. |
| `/winebodies` | Lists all wine body categories. |
| `/winebodies/<int:id>/` | Retrieves details of a specific wine body. |
| `/wineacidities` | Lists all wine acidity categories. |
| `/wineacidities/<int:id>/` | Retrieves details of a specific wine acidity. |
| `/wineries` | Lists all wineries. |
| `/wineries/<int:id>/` | Retrieves details of a specific winery. |
| `/regions` | Lists all wine regions. |
| `/regions/<int:id>/` | Retrieves details of a specific region. |
| `/users` | Lists all users who provided ratings. |
| `/users/<int:id>/` | Retrieves details of a specific user. |
| `/ratings` | Lists all wine ratings. |
| `/ratings/<int:id>/` | Retrieves details of a specific rating. |
| `/wine-details` | Provides complete details on wines, including average ratings. |
| `/search-wine` | Allows searching for wines by name. |
| `/wineryregion-stats` | Displays winery statistics by region. |
| `/best-portuguese-wines` | Lists the top 25 Portuguese wines based on ratings. |

### **Example SQL Queries**
#### **1. Retrieve Wine Details**
```sql
SELECT Wine.WineID, Wine.WineName, Wine.ABV, WineType.WineTypeName,
WineBody.WineBodyName, WineAcidity.WineAcidityName, Winery.WineryName,
Region.RegionName, AVG(Rating.WineRating) AS AvgRating, COUNT(Rating.RatingID) AS TotalRatings
FROM Wine
JOIN WineType ON Wine.TypeID = WineType.WineTypeID
JOIN WineBody ON Wine.BodyID = WineBody.WineBodyID
JOIN WineAcidity ON Wine.AcidityID = WineAcidity.WineAcidityID
JOIN Winery ON Wine.WineryID = Winery.WineryID
JOIN Region ON Wine.RegionID = Region.RegionID
LEFT JOIN Rating ON Wine.WineID = Rating.WineID
GROUP BY Wine.WineID
ORDER BY AvgRating DESC;
```
#### **2. Search for a Wine**
```sql
SELECT WineID, WineName, ABV FROM Wine WHERE WineName LIKE ?;
```
#### **3. Winery-Region Statistics**
```sql
SELECT Winery.WineryName, Region.RegionName, COUNT(DISTINCT Wine.WineID) as TotalWines,
AVG(Rating.WineRating) as AvgRating
FROM Winery
JOIN Wine ON Winery.WineryID = Wine.WineryID
JOIN Region ON Wine.RegionID = Region.RegionID
LEFT JOIN Rating ON Wine.WineID = Rating.WineID
GROUP BY Winery.WineryName, Region.RegionName
ORDER BY Winery.WineryName, Region.RegionName;
```
#### **4. Top 25 Portuguese Wines**
```sql
SELECT Wine.WineID, Wine.WineName, AVG(Rating.WineRating) as AvgRating
FROM Wine
JOIN Region ON Wine.RegionID = Region.RegionID
LEFT JOIN Rating ON Wine.WineID = Rating.WineID
WHERE Region.Country = 'Portugal'
GROUP BY Wine.WineID
HAVING AVG(Rating.WineRating) IS NOT NULL
ORDER BY AvgRating DESC
LIMIT 25;
```
