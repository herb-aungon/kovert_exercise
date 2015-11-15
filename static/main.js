var url = "http://herbportal.ddns.net/"
//var url = "http://localhost:5000/"
$( document ).ready(function() {
    $('#filter_cal').click(function() {
	
	var cal = 700;

	//run each function for every td with calories class
	$('tr td.calories').each(function() {
	    
	    // get value for td with class calories
	    if ($(this).text() < cal) 
	    {
		$(this).parent().hide();
	    }
	})
	    console.log(cal);  
    });

    $('#highlight_price').click(function() {
	
	var price = 8;

	//run each function for every td with calories class
	$('tr td.price').each(function() {
	    var t =$(this).text();
	    var t1 = t.split("$")
	    console.log(t1[1]);
	    // get value for td with class calories
	    if (t1[1] > price) 
	    {
		$(this).parent().css("background-color","red");
		}
	})
	console.log("tr color changed to yellow");
    });

    $("#home").click(function() {
    window.location.href = url + "kovert_exercise";
	console.log(url);
    });

    $("#food").click(function() {
	window.location.href = url + "kovert_exercise/food_items";
	console.log(url);
    });

});
