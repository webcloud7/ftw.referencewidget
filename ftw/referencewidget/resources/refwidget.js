$(function() {
    $('.referencewidget button').bind('click', openOverlay);

    function openOverlay(){
        var request_path = "";
        var url = window.location;
        var name = this.name;
        var widget_url = url + "++widget++" + name;
        var template = '<div class="refbrowser"><div class="path"></div><div class="listing"></div></div>';
        var node_template = '<span><a href="{{url}}">{{Title}}</a></span>';
        var listing_template = '<li class="ref_list_entry" data-path="{{path}}">{{checkbox}}{{title}}</li>';
        var checkbox = '<input type="chekbox" name="reference" value="{{value}}"';
        current_data = $.post
    }

});