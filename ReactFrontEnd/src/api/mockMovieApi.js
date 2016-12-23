import delay from './delay';

// This file mocks a web API by working with the hard-coded data below.
// It uses setTimeout to simulate the delay of an AJAX call.
// All calls return promises.


const movies = [
{
    "category": "Romance",
    "snapshot": "https://s3-us-west-2.amazonaws.com/sadmovie/no_string.jpg",
    "name": "No Strings Attached(2011)",
    "vid": "9yVrWNaBqpk",
    "playableUrl": "http://www.columbia.edu/",    
    "taskid": "79b264b70747327853bfa3979013faca",
    "authorId": "cory-house"

},
{
    "category": "Romance",
    "snapshot": "https://s3-us-west-2.amazonaws.com/sadmovie/no_string.jpg",
    "name": "No Strings Attached(2011)",
	"vid": "9yVrWNaBqpk1",
	"playableUrl": "http://www.columbia.edu/",    
    "taskid": "79b264b70747327853bfa3979013faca",
    "authorId": "cory-house"
},
{
    "category": "Romance",
    "snapshot": "https://s3-us-west-2.amazonaws.com/sadmovie/no_string.jpg",
    "name": "No Strings Attached(2011)",
	"vid": "9yVrWNaBqpk2",
	"playableUrl": "http://www.columbia.edu/",    
    "taskid": "79b264b70747327853bfa3979013faca",
    "authorId": "cory-house"
},
{
    "category": "Romance",
    "snapshot": "https://s3-us-west-2.amazonaws.com/sadmovie/no_string.jpg",
    "name": "No Strings Attached(2011)",
	"vid": "9yVrWNaBqpk3",
	"playableUrl": "http://www.columbia.edu/",    
    "taskid": "79b264b70747327853bfa3979013faca",
    "authorId": "cory-house"
},
{
    "category": "Romance",
    "snapshot": "https://s3-us-west-2.amazonaws.com/sadmovie/no_string.jpg",
    "name": "No Strings Attached(2011)",
	"vid": "9yVrWNaBqpk4",
	"playableUrl": "http://www.columbia.edu/",    
    "taskid": "79b264b70747327853bfa3979013faca",
    "authorId": "cory-house"
},
{
    "category": "Romance",
    "snapshot": "https://s3-us-west-2.amazonaws.com/sadmovie/no_string.jpg",
    "name": "No Strings Attached(2011)",
	"vid": "9yVrWNaBqpk5",
	"playableUrl": "http://www.columbia.edu/",    
    "taskid": "79b264b70747327853bfa3979013faca",
    "authorId": "cory-house"
}];

function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, 'g'), replace);
}

//This would be performed on the server in a real app. Just stubbing in.
const generateId = (movie) => {
  return replaceAll(movie.name, ' ', '-');
};

class MovieApi {
  static getAllMovies() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(Object.assign([], movies));
      }, delay);
    });
  }


static saveMovie(movie) {
movie = Object.assign({}, movie); // to avoid manipulating object passed in.
return new Promise((resolve, reject) => {
  setTimeout(() => {
    // Simulate server-side validation
    const minMovieTitleLength = 1;
    if (movie.name.length < minMovieTitleLength) {
      reject(`Title must be at least ${minMovieTitleLength} characters.`);
    }

    if (movie.vid) {
      const existingMovieIndex = movies.findIndex(a => a.vid == movie.vid);
      movies.splice(existingMovieIndex, 1, movie);

    } else {
      //Just simulating creation here.
      //The server would generate ids and watchHref's for new courses in a real app.
      //Cloning so copy returned is passed by value rather than by reference.
      movie.id = generateId(movie);
      movie.watchHref = `http://www.pluralsight.com/courses/${movie.id}`;
      movies.push(movie);
    }

    resolve(movie);
  }, delay);
});
}
}

export default MovieApi;
