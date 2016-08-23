(function(global, $, Handlebars) {


$(function() {

  $(document).on("click", ".referencewidget button", openOverlay);

  $(document).on("click", ".refbrowser .path span", jump_to);
  $(document).on("click", ".refbrowser .search button", search);
  $(document).on("keypress", ".refbrowser .search input", function(event){
    if(event.which == 13) {search(event);}});

  $(document).on("change", ".refbrowser .listing input.ref-checkbox", checkbox_flipped);
  $(document).on("click", ".refbrowser button.cancel", function(){$(".refbrowser").remove();});
  $(document).on("click", ".refbrowser .ref_list_entry", switch_level);
  $(document).on("click", ".refbrowser .listing input.ref-checkbox", function(e) {e.stopPropagation();});
  $(document).on("click", ".refbrowser .listing .refbrowser_batching a", change_page);
  var request_data = {};
//    var url = location.protocol + "//" + location.host + location.pathname;
  var widget_url = "";
  var field_id = "";
  var name = "";
  var list_template = "";
  var checkbox_template = "";
  var lookup_table = {};
  var request_path = "";
  var sel_type = "";
  var page = 1;
  $(".selected_items").each(function(){
    var container = $(this);
    var data = $(this).data("select");
    if (data === undefined){
      return;
    }
    data.forEach(function(item){
      item["title"] = item["title"] + " (" + item["path"] + ")";
      item["selectable"] = true;
      item["selected"] = "checked=\"checked\"";
      item["type"] = sel_type;
      item["checkbox"] = checkbox_template(item);
      $(container).find("ul").append(list_template(item));
    });
  });

  function openOverlay(e){
    $(".refbrowser").remove();
    list_template = Handlebars.compile($("#listing-template").html());
    checkbox_template = Handlebars.compile($("#checkbox-template").html());
    $(".sortable").sortable();

    var target = $(e.currentTarget);
    sel_type = target.closest(".referencewidget").data("type");
    field_id = target.closest(".field").attr("id");
    name = target.closest(".field").data("fieldname");
    widget_url = target.closest(".referencewidget").data("url") + "/++widget++" + name;
    $("body").append($("#refbrowser-template").html());
    build_pathbar("");
    get_data("");
  }

  function search(e){
    var value = $(e.currentTarget.parentNode).find("input:text").val();
    $.post(widget_url + "/search_for_refs", {"term": value}, function(data){
      rebuild_listing(data);
    });
  }

  function build_pathbar(path){
    $(".refbrowser .path").empty();
    $.post(widget_url +"/generate_pathbar", {"origin": path}, function(data){
      var hb_template = Handlebars.compile($("#node-template").html());
      var pathbar = "";
      data.forEach(function(item){
        pathbar += hb_template(item);
      });
      $(".path").append(pathbar);
    });

  }

  function switch_level(e){
    var ident = $(e.currentTarget).data("id");
    var path = request_data["items"][lookup_table[ident]]["path"];
    request_path = path;
    build_pathbar(path);
    get_data(path);
  }

  function change_page(e){
    var target = $(e.currentTarget);
    if (target.hasClass("next")){
      page++;
    }
    else if (target.hasClass("previous")){
      page--;
    }
    else{
      page = parseInt(target.text());
    }
    get_data(request_path, page);
  }

  function rebuild_listing(data){
    $(".refbrowser .listing ul").empty();
    var list_html = "";
    lookup_table = {};
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        var item = data[key];
        lookup_table[item["id"]] = key;
        item["selected"] = "";
        var is_selected = $(".referencewidget .selected_items li[data-path=\"" + item["path"] + "\"]");
        if (is_selected.length > 0) {
          item["selected"] = "checked=\"checked\"";
        }

        if (item["selectable"]){
          item["type"] = sel_type;
          item["checkbox"] = checkbox_template(item);
        }
        list_html += list_template(item);
      }
    }
    $(".listing ul").append(list_html);
  }

  function build_list(data){
    $(".refbrowser .refbrowser_batching").remove();
    var batch_template = Handlebars.compile($("#batch_template").html());
    $(".refbrowser .listing").append(batch_template(data));
    rebuild_listing(data["items"]);
  }

  function get_data(path, page){
    if (page === undefined){
      page = 1;
    }
    $.post(widget_url+"/get_reference_data", {"start": path, "page": page}, function(data){
      request_data = data;
      build_list(request_data);
    });
  }

  function jump_to(e){
    var path = $(e.currentTarget).data("path");
    if ($(e.currentTarget).data("clickable") === 1){
      request_path = path;
      build_pathbar(path);
      get_data(path);
    }
  }

  function checkbox_flipped(e){
    e.stopPropagation();
    var checkbox = e.currentTarget;
    if (checkbox.checked === true){
      var node = $(e.currentTarget.parentNode).clone();
      $(node).find("input").attr("name", name);
      var text = $.trim(node.find("span").text());
      text = text + " (" + node.data("path") + ")";
      node.find("span").text(text);
      $("#" + field_id + " .referencewidget .selected_items ul").append(node);
    }
    else {
      var query = "#" + field_id + " .referencewidget .selected_items li[data-path=\"" + $(e.currentTarget.parentNode).data("path") + "\"]";
      $(query).remove();
    }
  }

});


})(window, window.jQuery, window.Handlebars);
