$(function() {
    if ($('.referencewidget').length === 0){
        return;
    }
    $('.referencewidget button').bind('click', openOverlay);
    $('.sortable').sortable();
    var request_data = {}
    var url = window.location;
    var widget_url = ""
    var field_id = ""
    var name = ""
    var list_template = Handlebars.compile($('#listing-template').html());
    var checkbox_template = Handlebars.compile($('#checkbox-template').html());
    var batchsize = 20;
    var lookup_table = {}
    var request_path = ""
    var selected_containers = $('.selected_items').each(function(){
        var container = $(this);
        var data = $(this).data('select');
        if (data === undefined){
            return;
        }
        data.forEach(function(item){
            item['title'] = item['title'] + ' (' + item['path'] + ')';
            item['selectable'] = true;
            item['selected'] = 'checked="checked"';
            item['checkbox'] = checkbox_template(item);
            $(container).find('ul').append(list_template(item));
        });
    });

        $(this).find('input:text').autocomplete({source: widget_url + "/search_for_refs", minLength: 3, select: function(event, ui){
            var item = ui['item'];
            item['title'] = item['label']
            item['path'] = item['value']
            item['selectable'] = true;
            item['selected'] = 'checked="checked"';
            item['checkbox'] = checkbox_template(item);
            $(this).closest('.field').find('.selected_items ul').append(list_template(item));
            $(this).val('');
        }});

    function openOverlay(){
        field_id = $(this).closest('.field').attr('id');
        name = $(this).closest('.field').data('fieldname');
        widget_url = url + "/++widget++" + field_id.replace("formfield-form-widgets-", "");

        $('body').append($("#refbrowser-template").html());
        build_pathbar("");
        get_data("");
//        build_list(request_data);
    }

function search(e){
    var value = e.currentTarget.value;
    if (value.length < 3){
        return;
    }
    $.post(widget_url + '/search_for_refs', {'term': value}, function(data){
        rebuild_listing(JSON.parse(data));
    })
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
    $('.refbrowser .search input').bind('input', search);

    });

}

function switch_level(e){
    var ident = $(e.currentTarget).data('id');
    var path = request_data['items'][lookup_table[ident]]['path']
    request_path = path;
    build_pathbar(path);
    get_data(path);
    }

function change_page(e){
    $('.refbrowser_batching .batch').removeClass("active_batch");
    $(e.currentTarget).addClass("active_batch");
    get_data(request_path, parseInt($(e.currentTarget).text()));
}

function rebuild_listing(data){
    $('.refbrowser .listing ul').empty();
    var list_html = "";
    lookup_table = {}
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            var item = data[key];
            lookup_table[item['id']] = key;
            item['selected'] = "";
            var is_selected = $('.referencewidget .selected_items li[data-path="' + item['path'] + '"]');
            if (is_selected.length > 0) {
                item['selected'] = 'checked="checked"';
            }

            if (item['selectable']){
                item['checkbox'] = checkbox_template(item);
            }
            list_html += list_template(item);
        }
    }
    $('.listing ul').append(list_html);
    registerListingEvents();

}

function build_list(data){
            $('.refbrowser .refbrowser_batching').remove();
            if (data['count'] > data['batchsize']){
                var batch_template = Handlebars.compile($("#batch_template").html());
                var page_template = Handlebars.compile($("#page_template").html());
                $('.refbrowser .listing').append(batch_template());
                var pages = Math.ceil(data['count'] / data['batchsize']);
                for (var i=0;i<pages;i++){
                    $('.refbrowser .listing .refbrowser_batching').append(page_template({'page': i+1}));
                }
                $('.refbrowser_batching .batch').bind('click', change_page);
                $($('.refbrowser_batching .batch')[0]).addClass("active_batch");

            }
            rebuild_listing(data['items']);
}
function get_data(path, page){
        if (page === undefined){
            page = 1;
        }
        $.post(widget_url+'/get_reference_data', {'start': path, 'page': page}, function(data){
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

function checkbox_flipped(e){
    e.stopPropagation();
    var checkbox = e.currentTarget;
    if (checkbox.checked === true){
        var node = $(e.currentTarget.parentNode).clone();
        $(node).find('input').attr("name", name);
        text = $.trim(node.find('span').text());
        text = text + ' (' + node.data('path') + ')';
        node.find('span').text(text);
        $('#' + field_id + ' .referencewidget .selected_items ul').append(node)
    }
    else {
        var query = '#' + field_id + ' .referencewidget .selected_items li[data-path="' + $(e.currentTarget.parentNode).data("path") + '"]'
        $(query).remove();
    }
}

function registerListingEvents(){
    $('.refbrowser .listing input.ref-checkbox').bind('change', checkbox_flipped);
    $('.refbrowser button.cancel').bind('click', function(){$('.refbrowser').remove()});
    $('.ref_list_entry').bind('click', switch_level);
    $('.refbrowser .listing input.ref-checkbox').bind('click', function(e) {e.stopPropagation();})
    }


});
