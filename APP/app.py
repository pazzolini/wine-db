import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, request
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) n_wines FROM Wine)
    JOIN
      (SELECT COUNT(*) n_regions FROM Region)
    JOIN
      (SELECT COUNT(*) n_wineries FROM Winery)
    JOIN 
      (SELECT COUNT(*) n_users FROM User)
    JOIN 
      (SELECT COUNT(*) n_ratings FROM Rating)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)


# Wines
@APP.route('/wines/')
def list_wines():
    wines = db.execute(
      '''
      SELECT WineID, WineName, ABV
      FROM Wine
      ORDER BY WineName
      ''').fetchall()
    return render_template('wine-list.html', wines=wines)

@APP.route('/wines/<int:id>/')
def get_wine(id):
  wine = db.execute(
      '''
      SELECT WineID, WineName, ABV
      FROM Wine
      WHERE WineID = ?
      ''', [id]).fetchone()

  if wine is None:
     abort(404, 'Wine id {} does not exist.'.format(id))
         
  return render_template('wine-details.html', wine=wine)


#Wine Type
@APP.route('/winetypes/')
def list_wine_types():
    wine_types = db.execute(
        'SELECT WineTypeID, WineTypeName FROM WineType ORDER BY WineTypeID'
    ).fetchall()
    return render_template('winetype-list.html', wine_types=wine_types)
    
@APP.route('/winetypes/<int:id>/')
def get_wine_type(id):
    wine_type = db.execute(
        'SELECT WineTypeID, WineTypeName FROM WineType WHERE WineTypeID = ?', [id]
    ).fetchone()

    if wine_type is None:
        abort(404, 'WineType id {} does not exist.'.format(id))

    return render_template('winetype-details.html', wine_type=wine_type)


#Wine Body
@APP.route('/winebodies/')
def list_wine_bodies():
    wine_bodies = db.execute(
        'SELECT WineBodyID, WineBodyName FROM WineBody ORDER BY WineBodyID'
    ).fetchall()
    return render_template('winebody-list.html', wine_bodies=wine_bodies)

@APP.route('/winebodies/<int:id>/')
def get_wine_body(id):
    wine_body = db.execute(
        'SELECT WineBodyID, WineBodyName FROM WineBody WHERE WineBodyID = ?', [id]
    ).fetchone()

    if wine_body is None:
        abort(404, 'WineBody id {} does not exist.'.format(id))

    return render_template('winebody-details.html', wine_body=wine_body)


#Wine Acidty    
@APP.route('/wineacidities/')
def list_wine_acidities():
    wine_acidities = db.execute(
        'SELECT WineAcidityID, WineAcidityName FROM WineAcidity ORDER BY WineAcidityID'
    ).fetchall()
    return render_template('wineacidity-list.html', wine_acidities=wine_acidities)

@APP.route('/wineacidities/<int:id>/')
def get_wine_acidity(id):
    wine_acidity = db.execute(
        'SELECT WineAcidityID, WineAcidityName FROM WineAcidity WHERE WineAcidityID = ?', [id]
    ).fetchone()

    if wine_acidity is None:
        abort(404, 'WineAcidity id {} does not exist.'.format(id))

    return render_template('wineacidity-details.html', wine_acidity=wine_acidity)
 
 
# Wineries
@APP.route('/wineries/')
def list_wineries():
    wineries = db.execute(
        'SELECT WineryID, WineryName, Website FROM Winery ORDER BY WineryName'
    ).fetchall()
    return render_template('winery-list.html', wineries=wineries)

@APP.route('/wineries/<int:id>/')
def get_winery(id):
    winery = db.execute(
        'SELECT WineryID, WineryName, Website FROM Winery WHERE WineryID = ?', [id]
    ).fetchone()

    if winery is None:
        abort(404, 'Winery id {} does not exist.'.format(id))

    return render_template('winery-details.html', winery=winery)
    
    
# Regions    
@APP.route('/regions/')
def list_regions():
    regions = db.execute(
        'SELECT RegionID, RegionName, Country FROM Region ORDER BY RegionName'
    ).fetchall()
    return render_template('region-list.html', regions=regions)

@APP.route('/regions/<int:id>/')
def get_region(id):
    region = db.execute(
        'SELECT RegionID, RegionName, Country FROM Region WHERE RegionID = ?', [id]
    ).fetchone()

    if region is None:
        abort(404, 'Region id {} does not exist.'.format(id))

    return render_template('region-details.html', region=region)


# Winery / Regions
@APP.route('/wineryregions/')
def list_winery_regions():
    winery_regions = db.execute(
        '''
        SELECT WineryRegion.WineryID, WineryRegion.RegionID, Winery.WineryName, Region.RegionName
        FROM WineryRegion
        JOIN Winery ON WineryRegion.WineryID = Winery.WineryID
        JOIN Region ON WineryRegion.RegionID = Region.RegionID
        ORDER BY Winery.WineryName, Region.RegionName
        '''
    ).fetchall()
    return render_template('wineryregion-list.html', winery_regions=winery_regions)

@APP.route('/wineryregions/<int:winery_id>/<int:region_id>/')
def get_winery_region(winery_id, region_id):
    winery_region = db.execute(
        '''
        SELECT WineryRegion.WineryID, WineryRegion.RegionID, Winery.WineryName, Region.RegionName
        FROM WineryRegion
        JOIN Winery ON WineryRegion.WineryID = Winery.WineryID
        JOIN Region ON WineryRegion.RegionID = Region.RegionID
        WHERE WineryRegion.WineryID = ? AND WineryRegion.RegionID = ?
        ''', [winery_id, region_id]
    ).fetchone()

    if winery_region is None:
        abort(404, 'WineryRegion with WineryID {} and RegionID {} does not exist.'.format(winery_id, region_id))

    return render_template('wineryregion-details.html', winery_region=winery_region)
    
# Users
@APP.route('/users/')
def list_users():
    users = db.execute(
        'SELECT UserID FROM User ORDER BY UserID'
    ).fetchall()
    return render_template('user-list.html', users=users)

@APP.route('/users/<int:id>/')
def get_user(id):
    user = db.execute(
        'SELECT UserID FROM User WHERE UserID = ?', [id]
    ).fetchone()

    if user is None:
        abort(404, 'User id {} does not exist.'.format(id))

    return render_template('user-details.html', user=user)


# Ratings
@APP.route('/ratings/')
def list_ratings():
    ratings = db.execute(
        '''
        SELECT RatingID, WineID, UserID, WineRating, RatingDate
        FROM Rating
        ORDER BY RatingDate DESC
        '''
    ).fetchall()
    return render_template('rating-list.html', ratings=ratings)

@APP.route('/ratings/<int:id>/')
def get_rating(id):
    rating = db.execute(
        '''
        SELECT RatingID, WineID, UserID, WineRating, RatingDate
        FROM Rating
        WHERE RatingID = ?
        ''', [id]
    ).fetchone()

    if rating is None:
        abort(404, 'Rating id {} does not exist.'.format(id))

    return render_template('rating-details.html', rating=rating)


# Additional endpoint 1 
@APP.route('/wine-details/')
def wine_details_complete():
    wine_details = db.execute(
        '''
        SELECT Wine.WineID, Wine.WineName, Wine.ABV, WineType.WineTypeName, WineBody.WineBodyName, 
               WineAcidity.WineAcidityName, Winery.WineryName, Region.RegionName, 
               AVG(Rating.WineRating) AS AvgRating, COUNT(Rating.RatingID) AS TotalRatings
        FROM Wine
        JOIN WineType ON Wine.TypeID = WineType.WineTypeID
        JOIN WineBody ON Wine.BodyID = WineBody.WineBodyID
        JOIN WineAcidity ON Wine.AcidityID = WineAcidity.WineAcidityID
        JOIN Winery ON Wine.WineryID = Winery.WineryID
        JOIN Region ON Wine.RegionID = Region.RegionID
        LEFT JOIN Rating ON Wine.WineID = Rating.WineID
        GROUP BY Wine.WineID, Wine.WineName, Wine.ABV, WineType.WineTypeName, WineBody.WineBodyName, 
                 WineAcidity.WineAcidityName, Winery.WineryName, Region.RegionName
        ORDER BY AvgRating DESC
        '''
    ).fetchall()
    return render_template('wine-details-complete.html', wine_details=wine_details)

    
# Additional endpoint 2
@APP.route('/search-wine/', methods=['GET'])
def search_wine():
    query = request.args.get('query')
    if not query:
        return render_template('search-wine.html', wines=[])

    wines = db.execute(
        'SELECT WineID, WineName, ABV FROM Wine WHERE WineName LIKE ?', ['%' + query + '%']
    ).fetchall()
    return render_template('search-wine.html', wines=wines)
    
    
# Additional endpoint 3 
@APP.route('/wineryregion-stats/')
def winery_region_stats():
    stats = db.execute(
        '''
        SELECT Winery.WineryName, Region.RegionName, COUNT(DISTINCT Wine.WineID) as TotalWines, AVG(Rating.WineRating) as AvgRating
        FROM Winery
        JOIN Wine ON Winery.WineryID = Wine.WineryID
        JOIN Region ON Wine.RegionID = Region.RegionID
        LEFT JOIN Rating ON Wine.WineID = Rating.WineID
        GROUP BY Winery.WineryName, Region.RegionName
        ORDER BY Winery.WineryName, Region.RegionName
        '''
    ).fetchall()
    return render_template('wineryregion-stats.html', stats=stats)
    
# Additional endpoint 4
@APP.route('/best-portuguese-wines/')
def best_portuguese_wines():
    top_wines = db.execute(
        '''
        SELECT Wine.WineID, Wine.WineName, Wine.ABV, WineType.WineTypeName, WineBody.WineBodyName, 
               WineAcidity.WineAcidityName, Winery.WineryName, Region.RegionName, AVG(Rating.WineRating) as AvgRating
        FROM Wine
        JOIN WineType ON Wine.TypeID = WineType.WineTypeID
        JOIN WineBody ON Wine.BodyID = WineBody.WineBodyID
        JOIN WineAcidity ON Wine.AcidityID = WineAcidity.WineAcidityID
        JOIN Winery ON Wine.WineryID = Winery.WineryID
        JOIN Region ON Wine.RegionID = Region.RegionID
        LEFT JOIN Rating ON Wine.WineID = Rating.WineID
        WHERE Region.Country = 'Portugal'
        GROUP BY Wine.WineID, Wine.WineName, Wine.ABV, WineType.WineTypeName, WineBody.WineBodyName, 
                 WineAcidity.WineAcidityName, Winery.WineryName, Region.RegionName
        HAVING AVG(Rating.WineRating) IS NOT NULL
        ORDER BY AvgRating DESC
        LIMIT 25
        '''
    ).fetchall()
    return render_template('best-portuguese-wines.html', top_wines=top_wines)




    
    

