$(".card-title").text(function () {
    return $(this)
            .text()
            .replace(/(<([^>]+)>)/gi, "")
});

$(".card-text").text(function () {
    return $(this)
            .text()
            .replace(/(<([^>]+)>)/gi, "")
})


// save job to favorites
$(".favorites").on("click", function(evt) {
    evt.preventDefault();
    $(this).css("color", "green");
    let targetDiv = $(this).closest("div");
    let obj = targetDiv[0];
    let getHtml = obj.innerHTML;
    let res = getHtml.replace("Save Favorite Jobs","<button class='btn btn-sm btn-danger'>Delete</button>");
    let keyName = $(this).data("id");

    localStorage.setItem(keyName, res);
});

// get all storage data with all saved jobs
for (let i = 0; i < localStorage.length; i++) {
	 console.log(localStorage.key(i));
	$(".fav-jobs-list").append(localStorage.getItem(localStorage.key(i)) + "<hr />");
	$(".btn-danger").on("click", function () {
		window.location.reload();
		let closest = $(this).closest("a");
		let targetid = closest.attr("data-id");
		if (targetid === localStorage.key(i)) {
			localStorage.removeItem(targetid);
		}
        
	});
}