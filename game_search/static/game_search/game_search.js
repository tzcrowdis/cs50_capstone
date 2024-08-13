
document.addEventListener('DOMContentLoaded', function() {

    // manage path specific elements
    let path = window.location.pathname;
    let search = window.location.search;

    // hide content if no search results
    if (path === '/'){
        if (search === '') {

            // hide site templates
            document.getElementById('content-container').innerHTML = "";

            // hide search buttons
            document.getElementById('up').style.visibility = "hidden";
            document.getElementById('down').style.visibility = "hidden";
            document.getElementById('track').style.visibility = "hidden";
        } else{
    
            // display styled divs
            display_steam();
            display_abandonware();
            display_gog();
            animation_delays();

            // setup page navigation for search results
            document.getElementById('up').style.visibility = "hidden"; // assumes starting at top of page
            portal_height = document.getElementById('steam').scrollHeight;
            document.addEventListener("scroll", () => page_nav_manager());

            // set tracked button
            check_tracked();
        }
    }
    else {

        // hide search buttons
        document.getElementById('up').style.visibility = "hidden";
        document.getElementById('down').style.visibility = "hidden";
        document.getElementById('track').style.visibility = "hidden";
    }

    console.log("Loaded");
});


// arrow keys switch between results
document.onkeydown = function (e) {

    switch (e.key) {
        case 'ArrowUp':
            e.preventDefault();        
            document.getElementById('up').click();
            break;
        case 'ArrowDown':
            e.preventDefault();        
            document.getElementById('down').click();
            break;
    }
};


function page_nav_manager() {

    scrollPos = window.scrollY;

    // change next and previous buttons based on location
    let previous = document.getElementById('up');
    let next = document.getElementById('down');

    // real values eyeballed
    // 0 to portal height
    if (scrollPos < 0.75 * portal_height){

        // hide previous
        previous.style.visibility = "hidden";
        // set next to abandonware
        next.href = "#middle";
    } // 1x to 2x portal height
    else if (0.75 * portal_height <= scrollPos && scrollPos <= 1.5 * portal_height) {
        
        // show previous and next
        previous.style.visibility = "visible";
        next.style.visibility = "visible";
        // set previous to steam aka top
        previous.href = "#top";
        // set next to gog
        next.href = "#bottom";
    } // greater than 2x portal height
    else {

        // hide next
        next.style.visibility = "hidden";
        // set previous to abandonware
        previous.href = "#middle";
    }
}


function display_loading() {

    // hide previous results
    document.getElementById('content-container').innerHTML = "";
    // show loading animation until search results load
    document.getElementById('loading').style.visibility = "visible";
}


function animation_delays() {

    // adjust animation delay based on ordering
    // ignoring abandonware bc its always last
    try {
        var steam_height = document.getElementById('steam').getBoundingClientRect().top;
    } catch(err) { var steam_height = 0; }
    try {
        var gog_height = document.getElementById('gog').getBoundingClientRect().top;
    } catch(err) { var gog_height = 0; }

    if (gog_height < steam_height) {
        try {
            document.getElementById('gog').style.animationDelay = "0s";
            document.getElementById('gog-ripple-1').style.animationDelay = "1s";
            document.getElementById('gog-ripple-2').style.animationDelay = "2s";
            document.getElementById('gog-ripple-3').style.animationDelay = "3s";
        } catch(err) {}

        try {
            document.getElementById('steam').style.animationDelay = "0.75s";
            document.getElementById('steam-ripple-1').style.animationDelay = "1.75s";
            document.getElementById('steam-ripple-2').style.animationDelay = "2.75s";
            document.getElementById('steam-ripple-3').style.animationDelay = "3.75s";
        } catch(err) {}
    } else {
        try {
            document.getElementById('steam').style.animationDelay = "0s";
            document.getElementById('steam-ripple-1').style.animationDelay = "1s";
            document.getElementById('steam-ripple-2').style.animationDelay = "2s";
            document.getElementById('steam-ripple-3').style.animationDelay = "3s";
        } catch(err) {}

        try {
            document.getElementById('gog').style.animationDelay = "0.75s";
            document.getElementById('gog-ripple-1').style.animationDelay = "1.75s";
            document.getElementById('gog-ripple-2').style.animationDelay = "2.75s";
            document.getElementById('gog-ripple-3').style.animationDelay = "3.75s";
        } catch(err) {}
    }
}


function display_steam() {

    try {
        // grab steam variables
        let title = document.getElementById("steam-title").innerHTML;
        let image = document.getElementById("steam-image").innerHTML;
        let description = document.getElementById("steam-description").innerHTML;
        let price = document.getElementById("steam-price").innerHTML;
        let link = document.getElementById("steam-link").innerHTML;

        //insert styled steam html
        let steam = `<div id="steam-ripple-1" class="rippler"></div>
                <div id="steam-ripple-2" class="rippler"></div>
                <div id="steam-ripple-3" class="rippler"></div>

                <div id="steam-title">` + title + `</div>
                <img id="steam-image" src="` + image + `">
                <div id="steam-description">` + description + `</div>

                <div id="steam-price-container1">
                    Play ` + title + `
                    <div id="steam-price-container2">
                        <div id="steam-price">` + price + `</div>
                        <a id="steam-link" href="` + link + `" target="_blank">
                            Visit Steam
                        </a>
                    </div>
                </div>`;

        document.getElementById('steam').innerHTML = steam;
    } catch(err) {}
}


function display_abandonware() {

    try {
        // grab abandonware variables
        let title = document.getElementById("abandonware-title").innerHTML;
        let image = document.getElementById("abandonware-image").innerHTML;
        let description = document.getElementById("abandonware-description").innerHTML;
        let link = document.getElementById("abandonware-link").innerHTML;

        //insert styled abandonware html
        let abandonware = `<div id="abandonware-ripple-1" class="rippler"></div>
                <div id="abandonware-ripple-2" class="rippler"></div>
                <div id="abandonware-ripple-3" class="rippler"></div>

                <div style="height: 100%;">
                    <div id="abandonware-title">` + title + `</div>
                    <hr class="ab-divider">
                    <img id="abandonware-image" src="` + image + `">
                    <hr class="ab-divider">
                    <div id="abandonware-description">
                        <h3 id="ab-desc-header">Description of ` + title + `</h3>
                            ` + description + `
                    </div>
                    <a href="` + link +`" id="abandonware-link" target="_blank">
                        VISIT MY ABANDONWARE
                    </a>
                </div>`;

        document.getElementById('abandonware').innerHTML = abandonware;
    } catch(err) {}
}


function display_gog() {

    try {
        // grab gog variables
        let title = document.getElementById("gog-title").innerHTML;
        let image = document.getElementById("gog-image").innerHTML;
        let description = document.getElementById("gog-description").innerHTML;
        let price = document.getElementById("gog-price").innerHTML;
        let link = document.getElementById("gog-link").innerHTML;

        //insert styled gog html
        let gog = `<div id="gog-ripple-1" class="rippler"></div>
                <div id="gog-ripple-2" class="rippler"></div>
                <div id="gog-ripple-3" class="rippler"></div>

                <div id="gog-shadow-hider">
                    <img id="gog-image" src="` + image + `">
                    <div id="gog-shadow-container">
                        <div id="gog-title">` + title + `</div>
                        <div id="gog-price-container">
                            <div id="gog-price">` + price + `</div>
                            <a href="` + link + `" id="gog-link" target="_blank">
                                Visit GOG
                            </a>
                        </div>
                        <div id="gog-description">` + description + `</div>
                    </div>
                </div>`;

        document.getElementById('gog').innerHTML = gog;
    } catch(err) {}
}


function track_results(){

    // get query
    let search_query = window.location.search;
    search_query = String(search_query).slice(6).replaceAll("+", " ");

    // get title and prices
    let steam_title = "";
    let steam_price = "";
    try {
        steam_title = document.getElementById('steam-title').textContent;
        steam_price = document.getElementById('steam-price').textContent;
    } catch(err) {}

    let aband_title = "";
    let aband_price = "";
    try {
        aband_title = document.getElementById('abandonware-title').textContent;
        aband_price = "Free";
    } catch(err) {}

    let gog_title = "";
    let gog_price = "";
    try {
        gog_title = document.getElementById('gog-title').textContent;
        gog_price = document.getElementById('gog-price').textContent;
    } catch(err) {}

    let btn = document.getElementById('track');
    if (btn.textContent === "Track"){

        // send data to backend
        fetch('/track_untrack', {
            method: 'POST',
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            body: JSON.stringify({
                status: "track",
                query: search_query,
                steam: [steam_title, steam_price],
                abandonware: [aband_title, aband_price],
                gog: [gog_title, gog_price]
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.response_status === "success") {
                // change styling
                btn.textContent = "Untrack";
                btn.style.color = "black";
                btn.style.backgroundColor = "whitesmoke";
            }
        });
    }
    else if (btn.textContent === "Untrack"){

        // send untrack data
        fetch('/track_untrack', {
            method: 'POST',
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            body: JSON.stringify({
                status: "untrack",
                query: search_query
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.response_status === "success") {
                // change styling
                btn.textContent = "Track";
                btn.style.color = "whitesmoke";
                btn.style.backgroundColor = "black";
            }
        });
    }
}


function check_tracked() {

    // get search query
    let search_query = window.location.search;
    search_query = String(search_query).slice(6).replaceAll("+", " ");

    let btn = document.getElementById('track');

    // checks if tracked on page load and sets button accordingly
    fetch('/check_tracked', {
        method: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({
            query: search_query
        })
    })
    .then(response => response.json())
    .then(result => {
        try{
            if (result.response_status === "untracked") {

                // track styling
                btn.textContent = "Track";
                btn.style.color = "whitesmoke";
                btn.style.backgroundColor = "black";
            }
            else if (result.response_status === "tracked") {

                // untrack styling
                btn.textContent = "Untrack";
                btn.style.color = "black";
                btn.style.backgroundColor = "whitesmoke";
            }
        }
        catch(err) {
            // do nothing, button hidden
        }
    });
}


function go_to_query(query) {

    // navigates to search query from tracked list
    query = query.replaceAll(" ", "+");
    window.location.href = "http://127.0.0.1:8000/" + "?game=" + query; //TODO: change to real domain
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}