function processForm(e) {
    e.preventDefault()
    $.ajax ({
        method: "POST",
        url: "http://localhost:5000/users/search-job",
        contentType: "application/json",
        data: JSON.stringify({
            title: $("#title").val(),
            location: $("#location").val()
        }),
        success: handleResponse
       
    });
};

function handleResponse(resp) {
  console.log(resp)
  for (let result in resp['results']) {
      `<div class="card">
        <div> class="card-body">
        <h4 class="card-title">${result.title} up to ${result.salary_max}</h4>
        <h5>${result.location.display_name}</h5>
        <h5>${result.company.display_name}
        <p class="card-test">${result.description}</p>
        <a href="${result.redirect_url}">View Job</a>
        </div>
       </div> `;
  } 
    
}


$("#search-form").on("submit", processForm)


