$(function() {
    $('.referencewidget button').bind('click', openOverlay);
    var request_data = {}
    var url = window.location;
    var widget_url = ""
    function openOverlay(){
        var name = $(this).closest('.field').attr('id');
        widget_url = url + "/++widget++" + name.replace("formfield-form-widgets-", "");

        $('body').append($("#refbrowser-template").html());
        build_pathbar("");
        get_data("");
//        build_list(request_data);
    }

function build_pathbar(path){
    $('.refbrowser .path').empty();
    var pathbar = $.post(widget_url +'/generate_pathbar', {'origin': path}, function(data){
    var hb_template = Handlebars.compile($("#node-template").html());
    var pathbar = '';
    JSON.parse(data).forEach(function(item){
        pathbar += hb_template(item);
    });
    $('.path').append(pathbar);
    $('.refbrowser .path span').bind('click', jump_to);

    });

}

function switch_level(e){
    var ident = $(e.currentTarget).data('id');
    if (!$.isEmptyObject(request_data[ident]['children'])){
        build_list(request_data[ident]['children']);
        build_pathbar(request_data[ident]['path']);
        get_data(request_data[ident]['path']);
    }
}

function build_list(data){
            $('.refbrowser .listing ul').empty();
            var list_html = "";
            var list_template = Handlebars.compile($('#listing-template').html());
            var checkbox_template = Handlebars.compile($('#checkbox-template').html());
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    var item = data[key];
                    if (item['selectable']){
                        item['checkbox'] = checkbox_template(item);
                    }
                    list_html += list_template(item);
                }
        }
            $('.listing ul').append(list_html);
            registerListingEvents();

}

function get_data(path){
        $.post(widget_url+'/get_reference_data', {'start': path}, function(data){
            data = JSON.parse(data);
            request_data = data;
            build_list(request_data);

        });
}

function jump_to(e){
    var path = $(e.currentTarget).data('path');
    build_pathbar(path);
    get_data(path);
}

function registerListingEvents(){
    $('.refbrowser button.cancel').bind('click', function(){$('.refbrowser').remove()});
    $('.ref_list_entry').bind('click', switch_level);
//        $('.refbrowser .listing input.ref-checkbox').bind('change', checkbox_fliped());
    }


});
