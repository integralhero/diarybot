var PythonShell = require('python-shell');

// Helper method
function str_arr_to_object(results, callback) {
	console.log(results);
	var object = {};
	for (var i = 0; i < results.length; i++)
	{
		var keyValue = results[i].replace(/[\r]+/g, '').split("\t");
		object[keyValue[0]] = keyValue[1];
	}
	console.log(object);
	callback(object);
}

// text is the string of the entry
// callback is a callback function that takes in the object of pronoun usage
function get_pronoun_usage(text, callback)
{
	var options = {
		scriptPath: './python',
		args: ["pronoun", text]
	};
	var filename = 'summarization.py';
	PythonShell.run(filename, options, function (err, results) {
		if (err) throw err;
		str_arr_to_object(results, callback);
	});
}

// text = "I'm twelve years old and what is this? Who are you? Who am I? Why am I writing this story here?";
// get_pronoun_usage(text);