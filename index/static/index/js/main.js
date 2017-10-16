// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.onload = function() {
    var csrftoken = getCookie('csrftoken');
    //This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post

    $.ajax({
    url : window.location.href, // the endpoint,commonly same url
    type : "POST", // http method
    data : { csrfmiddlewaretoken : csrftoken,
        request_type : "available"
    }, // data sent with the post request

           // handle a successful response
           success : function(json) {
               console.log(json); // another sanity check
               json = json.replace(/'/g, '"');
               variables.available = JSON.parse(json);
           },

           // handle a non-successful response
           error : function(xhr,errmsg,err) {
               console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
           }
    });
};

variables = {
    available : [],
    components : [],
}

$(document).ready(function() {
    $('#save-to-user').click(function(event) {
        var csrftoken = getCookie('csrftoken');
        event.preventDefault();
        var query = {
            csrfmiddlewaretoken : csrftoken,
            request_type : "save-to-user",
            username : document.getElementById('username').value,
            password : document.getElementById('password').value,
            width : variables.width,
            height : variables.height,
            component_names : [],
            component_xs : [],
            component_ys : [],
        }

        for(c in variables.components) {
            console.log(c);
            console.log("var.comptan ekle "+variables.components[c]['name']);
            console.log("var.comptan ekle "+variables.components[c]['x']);
            console.log("var.comptan ekle "+variables.components[c]['y']);
            query['component_names'].push(variables.components[c]['name']);
            query['component_xs'].push(variables.components[c]['x']);
            query['component_ys'].push(variables.components[c]['y']);
        }

        $.post(window.location.pathname,
            query,
            function(data, status){
                if(data['result'] === 'fail') {
                    alert("User exists. Wrong password");
                }
                else {
                    window.location.href = "/"+query['username'];
                }
            });
    });

    $(document).on('click', '.component-add-button', function(event) {
        var select = $(this).parent().find('.comp-select')[0];
        var c = $(this).parent().find('.x-select')[0].value;
        var r = $(this).parent().find('.y-select')[0].value;
        var comp_name = select.options[select.selectedIndex].value;
        var csrftoken = getCookie('csrftoken');
        event.preventDefault();
        $.post(window.location.pathname,
            {
                csrfmiddlewaretoken : csrftoken,
                request_type : "add-component",
                comp_name : comp_name,
            },
            function(data, status){
                $("#r" + r + "c" + c).html(data["html"]);
                $("#r" + r + "c" + c).find("script").each(function(i) {
                eval($(this).text());});
                variables.components.push({
                    name : comp_name,
                    x : c,
                    y : r,
                });
            });
    });

    $('#add-component').click(function(event) {
        event.preventDefault();
        var comp_config = document.createElement('div');
        var comp_list = document.createElement('select');
        var x_list  = document.createElement('select');
        var y_list  = document.createElement('select');

        comp_list.className = 'comp-select';
        x_list.className = 'x-select';
        y_list.className = 'y-select';

        for (comp in variables.available) {
            var comp_option = document.createElement('option');
            comp_option.value = variables.available[comp];
            comp_option.innerHTML = variables.available[comp];
            comp_list.appendChild(comp_option);
        }

        for (i = 0; i < variables.width; i++)
        {
            var x_option = document.createElement('option');
            x_option.value = i;
            x_option.innerHTML = i+1;
            x_list.appendChild(x_option);
        }

        for (j = 0; j < variables.height; j++)
        {
            var y_option = document.createElement('option');
            y_option.value = j;
            y_option.innerHTML = j+1;
            y_list.appendChild(y_option);
        }

        var comp_add_button = document.createElement('button');
        comp_add_button.className = 'component-add-button';
        comp_add_button.innerHTML = '+';

        comp_config.appendChild(comp_list);
        comp_config.appendChild(y_list);
        comp_config.appendChild(x_list);
        comp_config.appendChild(comp_add_button);

        document.getElementById('component-adder').appendChild(comp_config);
    });

    $('#generate-dashboard').click(function(event) {
        event.preventDefault();
        var width  = document.getElementById('Width').value;
        var height = document.getElementById('Height').value;
        variables.width = width;
        variables.height = height;
        variables.components = [];
        // Delete component adding children of component-adder
        var c_adder = document.getElementById("component-adder");
        while (c_adder.childNodes.length > 2) {
            c_adder.removeChild(c_adder.lastChild);
        }
        // Delete all children first
        var c_container = document.getElementById("component-container");
        while (c_container.firstChild) {
            c_container.removeChild(c_container.firstChild);
        }
        // Fill with new ones
        for(i = 0; i < height; i++)
        {
            var row = document.createElement('div');
            row.id = 'row'+i;
            row.className = 'component-row';
            row.style.height = (100 / height - 1) + "%";
            for(j = 0; j < width; j++)
            {
                var cell = document.createElement('div');
                cell.id = 'r'+i+'c'+j;
                cell.innerHTML = 'component cell';
                cell.className = 'component-cell';
                cell.style.width = (100 / width - 1) + "%";
                cell.style.height = "100%";
                row.appendChild(cell);
            }
            document.getElementById('component-container').appendChild(row);
        }
    });
});
