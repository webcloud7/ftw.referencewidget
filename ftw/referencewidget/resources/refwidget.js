(function(global, $, Handlebars) {


  $(function() {


    function initRefBrowser(button){
      var widget = this;
      widget.button = $(button);
      var buttonSelector = '#' + widget.button.attr('id');

      $(document).off("click", buttonSelector);
      $(document).on("click", buttonSelector, widget.openOverlay.bind(null, widget));
      $(window).one("resize", widget.resize);

      $(document).one("keydown", function(event){
        if(event.which == 27){
          event.stopPropagation();
          overlayClose(event);
        }
      });

      $(document).on('click', function(event){
        // Close overlay if click was not within the overlay
        if(!$(event.target).closest('.refbrowser').length) {
          overlayClose(event);
        }
      });

      widget.field = widget.button.closest(".field");
      widget.name = widget.field.data("fieldname");

      widget.request_data = {};
      widget.widget_url = "";
      widget.field_id = "";
      widget.list_template = "";
      widget.checkbox_template = "";
      widget.request_path = "";
      widget.sel_type = "";
      widget.page = 1;
      widget.term = "";

      widget.list_template = Handlebars.compile($("#listing-template").html());
      widget.checkbox_template = Handlebars.compile($("#checkbox-template").html());
      widget.sel_type = widget.button.closest(".referencewidget").data("type");

      widget.loadSelectedItems(widget);

      $(document).on('OverlayContentReloaded', ".overlay", function(widget, event){
        widget.button = $('#' + widget.button.attr("id"));
        widget.loadSelectedItems(widget);
      }.bind(null, widget));
}

    initRefBrowser.prototype.loadSelectedItems = function(widget){
        var container = widget.button.siblings('.selected_items');
        if (!container.find('ul').is(':empty')){
          return;
        }
        var data = container.data("select");
        if (data !== undefined){
          data.forEach(function(widget, item){
            if (item["path"] === ""){
              return;
            }
            item["title"] = item["title"] + " (" + item["path"] + ")";
            item["selectable"] = true;
            item["traversable"] = false;
            item['addclass'] = "";
            item['tag'] = "span";
            item["selected"] = "checked=\"checked\"";
            item["type"] = widget.sel_type;
            item["name"] = widget.name;
            item["checkbox"] = widget.checkbox_template(item);
            $(container).find("ul").append(widget.list_template(item));
          }.bind(null, widget));
        }
    };

    initRefBrowser.prototype.openOverlay = function(widget, event){
      event.stopPropagation();
      event.preventDefault();
      $("body").addClass("RefBrowserOverlayOpened");
      widget.list_template = Handlebars.compile($("#listing-template").html());
      widget.checkbox_template = Handlebars.compile($("#checkbox-template").html());
      $(".sortable").sortable();

      var target = $(event.currentTarget);
      var container = target.closest(".referencewidget");
      widget.sel_type = container.data("type");
      widget.field_id = widget.field.attr("id");

      var translations = container.data("trans");
      widget.widget_url = container.data("url") + "/++widget++" + widget.name;
      var refbrowser_template = Handlebars.compile($("#refbrowser-template").html());
      $("body").append(refbrowser_template(translations));
      widget.build_pathbar(widget, "");
      widget.get_data(widget, "");

      var overlay = (".refbrowser");

      $(overlay).on("click", ".refbrowser .path a", widget.jump_to.bind(null, widget));
      $(overlay).on("click", ".refbrowser .search button", widget.search.bind(null, widget));
      $(overlay).on("keypress", ".refbrowser .search input", function(event){
        if(event.which == 13) {
          widget.search(widget, event);
      }});

      $(overlay).on("change", ".refbrowser .listing input.ref-checkbox", widget.checkbox_flipped.bind(null, widget));
      $(overlay).on("click", ".refbrowser button.cancel", function(){$(".refbrowser").remove();});
      $(overlay).on("click", ".refbrowser .ref_list_entry", widget.switch_level.bind(null, widget));
      $(overlay).on("click", ".refbrowser .listing input.ref-checkbox", function(e) {e.stopPropagation();});
      $(overlay).on("click", ".refbrowser .refbrowser_batching a", widget.change_page.bind(null, widget));

    };

    function overlayClose(event){
      $("body").removeClass("RefBrowserOverlayOpened");
      $(".refbrowser").remove();
    }

    initRefBrowser.prototype.search = function(widget, event){
      event.stopPropagation();
      event.preventDefault();

      var value = $(event.currentTarget.parentNode).find("input:text").val();
      widget.term = value;
      widget.page = 1;
      widget.search_results(widget);
    };

    initRefBrowser.prototype.search_results = function(widget){
      $.post(widget.widget_url + "/search_for_refs", {"term": widget.term, "page": widget.page}, function(widgett, data){
        $(".refbrowser .refbrowser_batching").remove();
        widget.build_list(widget, data);
        widget.request_data = data;
        $(".refbrowser .listing").addClass("search_result");
      }.bind(null, widget));

    };

    initRefBrowser.prototype.build_pathbar = function(widget, path){
      $.post(widget.widget_url +"/generate_pathbar", {"origin": path}, function(data){
        var hb_template = Handlebars.compile($("#node-template").html());
        var pathbar = "";
        data.forEach(function(item){
          pathbar += hb_template(item);
        });
        $(".path").html(pathbar);
      });

    };

    initRefBrowser.prototype.switch_level = function(widget, event){
      event.preventDefault();
      event.stopPropagation();

      var target = $(event.currentTarget);
      var traversable = target.data("traversable");
      if (traversable === false){
        return;
      }

      var path = target.data("path");
      widget.request_path = path;
      widget.build_pathbar(widget, path);
      widget.get_data(widget, path);
    };

    initRefBrowser.prototype.change_page = function(widget, event){
      var target = $(event.currentTarget);
      if (target.hasClass("next")){
        widget.page++;
      }
      else if (target.hasClass("previous")){
        widget.page--;
      }
      else{
        widget.page = parseInt(target.text());
      }
      var listing = target.closest('.formcontrols').siblings('.listing');
      if (listing.hasClass("search_result") === true){
        widget.search_results(widget, widget.page);
      }
      else{
        widget.get_data(widget, widget.request_path, widget.page);
      }
    };

    initRefBrowser.prototype.rebuild_listing = function (widget, data){
      $(".refbrowser .listing ul").empty();
      var list_html = "";
      for (var key in data) {
        if (data.hasOwnProperty(key)) {
          var item = data[key];
          item["selected"] = "";
          item["extras"] = "";
          item["tag"] = "span";
          item["name"] = widget.name;
          var is_selected = $(".referencewidget .selected_items li[data-path=\"" + item["path"] + "\"]", widget.field);
          if (is_selected.find("input:checked").length > 0) {
            item["selected"] = "checked=\"checked\"";
          }
          item["addclass"] = "";
          if (item["traversable"]){
            item["addclass"] = "traversable";
            item["tag"] = "a";
            item["extras"] = "href='#'";
          }
          if (item["selectable"]){
            item["type"] = widget.sel_type;
            item["checkbox"] = widget.checkbox_template(item);
          }
          list_html += widget.list_template(item);
        }
      }
      $(".listing ul").append(list_html);
    };

    initRefBrowser.prototype.build_list = function(widget, data){
      $(".refbrowser .refbrowser_batching").remove();
      var batch_template = Handlebars.compile($("#batch_template").html());
      $(".refbrowser .batchingcontainer").append(batch_template(data));
      $(".refbrowser .batchingcontainer .previous").html("&laquo;");
      $(".refbrowser .batchingcontainer .next").html("&raquo;");
      widget.rebuild_listing(widget, data["items"]);
      var height = $(".refbrowser .pathbar").outerHeight(true);
      $(".refbrowser .listing").css({ top: height + "px" });

    };

    initRefBrowser.prototype.get_data = function(widget, path, page){
      if (page === undefined){
        page = 1;
      }
      $.post(widget.widget_url+"/get_reference_data", {"start": path, "page": page}, function(widget, data){
        widget.request_data = data;
        widget.build_list(widget, widget.request_data);
      }.bind(null, widget));
    };

    initRefBrowser.prototype.jump_to = function(widget, event){
      event.stopPropagation();
      event.preventDefault();
      var item = $(event.currentTarget);
      var path = $(item).data("path");
      if ($(item).data("clickable")){
        widget.request_path = path;
        widget.build_pathbar(widget, path);
        widget.get_data(widget, path);
      }
    };

    initRefBrowser.prototype.resize = function(){
      $(".refbrowser .pathbar").each(function(item){
          var height = $(this).outerHeight(true);
          var listing = $(this).siblings(".listing");
          listing.css({"top": height + "px"});
        });
    };

    initRefBrowser.prototype.checkbox_flipped = function(widget, event){
      event.stopPropagation();
      event.preventDefault();

      var checkbox = event.currentTarget;
      if (checkbox.checked === true){
        var node = $(event.currentTarget.parentNode).clone();
        $(node).find("input").attr("name", widget.name);
        var text = $.trim(node.find("span").text());
        text = text + " (" + node.data("path") + ")";
        node.find("span").text(text);
        $("#" + widget.field_id + " .referencewidget .selected_items ul").append(node);
      }
      else {
        var query = "#" + widget.field_id + " .referencewidget .selected_items li[data-path=\"" + $(event.currentTarget.parentNode).data("path") + "\"]";
        $(query).remove();
      }
    };


    // Regular usecase
    $(window).on('load', function(event){
      var refButtons = $(".referencewidget button");
      if (refButtons.length !== 0){
        refButtons.each(function(index, button){
          new initRefBrowser(button);
        });
      }
    });    // Overlays

    $(document).on("onLoad", ".overlay", function(event){
      var refButtons = $(".referencewidget button", $(this));
      if (refButtons.length !== 0){
        refButtons.each(function(index, button){
          new initRefBrowser(button);
        });
      }
    });

    // Public api
    window.initRefBrowser = initRefBrowser;

  });


})(window, window.jQuery, window.Handlebars);
