CREATE TABLE WineType (
    WineTypeID INT PRIMARY KEY,
    WineTypeName VARCHAR(100)
);

CREATE TABLE WineBody (
    WineBodyID INT PRIMARY KEY,
    WineBodyName VARCHAR(100)
);

CREATE TABLE WineAcidity (
    WineAcidityID INT PRIMARY KEY,
    WineAcidityName VARCHAR(100)
);

CREATE TABLE Region (
    RegionID INT PRIMARY KEY,
    RegionName VARCHAR(100),
    Country VARCHAR(100)
);

CREATE TABLE Winery (
    WineryID INT PRIMARY KEY,
    WineryName VARCHAR(100),
    Website VARCHAR(100)
);

CREATE TABLE WineryRegion (
    WineryID INT,
    RegionID INT,
    PRIMARY KEY (WineryID, RegionID),
    FOREIGN KEY (WineryID) REFERENCES Winery(WineryID),
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID)
);

CREATE TABLE Wine (
    WineID INT PRIMARY KEY,
    WineName VARCHAR(100),
    ABV FLOAT,
    TypeID INT,
    BodyID INT,
    AcidityID INT,
    WineryID INT,
    RegionID INT,
    FOREIGN KEY (TypeID) REFERENCES WineType(WineTypeID),
    FOREIGN KEY (BodyID) REFERENCES WineBody(WineBodyID),
    FOREIGN KEY (AcidityID) REFERENCES WineAcidity(WineAcidityID),
    FOREIGN KEY (WineryID) REFERENCES Winery(WineryID),
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID)
);

CREATE TABLE User (
    UserID INT PRIMARY KEY
);

CREATE TABLE Rating (
    RatingID INT PRIMARY KEY,
    WineID INT,
    UserID INT,
    WineRating FLOAT,
    RatingDate DATETIME,
    FOREIGN KEY (WineID) REFERENCES Wine(WineID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);
