ftw.referencewidget
===================

This Widget provides a Referencebrowser and a searchfield, which allows users to select references.

The basequery is all types which are not in the types_not_searched property all modification to the allowed types are relative to this query.

Traversal or Selectability can be changed for all widgets with the IReferenceSettings registry interface or per widget with the widget parameters.

The widget takes the following parameters:
 - allow_traversal: List of Types which are added as traversable. Will act as complete configuration if `override` is set to True.
 - block_traversal: List of Types which are added as not traversable. Will be ignored if `override` is set to True.
 - selectable: List of Types which are added to the as selectable. Will act as complete configuration if `override` is set to True
 - nonselectable: List of Types which are added as not selectable. Will be ignored if `override` is set to True.
 - start: The path first opened. Can either be a callable or a path. Additionaly the strings "parent", "navroot", "ploneroot" can be used.
 - allow_nonsearched_types: If this is set to true all the types will be traversable and selectable.
 - override: Drops all global config and the base query if a list is passed to the widget. If this is set to true, `selectable` & `allow_traversal` are not additive but act as the complete configuration instead. `nonselectable` & `block_traversal` will be ignored.
 - traversal_query: Updates the query used vor traversing by the given dict. The dict passed will be updated after everything is allready done. So make sure not to override sort_on/sort_order attributes.
 - explicit_type_filter: Makes it possible to exclude certain types from showing at all. IMPORTAN: For this the restapi needs to support NOT queries: Like portal_type.not=Image. 


Usage
-----

- Add ``ftw.referencewidget`` to your buildout configuration or as dependency to your package:

.. code:: ini

    [instance]
    eggs +=
        ftw.referencewidget

- Install the default generic import profile.



Installation / Development
--------------------------

.. code:: sh

    $ make install
    $ make run


We support both option since the makefile approach does not support yet all the features
from the zope2instance recipe. For example control scripts are not yet supported
But it's faster and more convenient to setup a docker test image


Javascript development
----------------------

From version 4 the widget is based upon boorstrap 5.2 and Vuejs 3. It's not yet a pattern, but it might be possible to wrap it in a pattern.


.. code:: sh

    $ npm install


Develop JS

.. code:: sh

    $ npm run dev


Build for production:

.. code:: sh

    $ npm run build


Javascript public API:
----------------------

You can run "window.initReferenceWidget" in your code. It will scan for all referencebrowser widgets an if not yet initialized it will initialized the JS widget.


Upgrading from 1.x to 2.x
-------------------------

There was no version number set for the ``ftw.referencewidget`` package. As a result of this upgradesteps wont be shown in ``../@@manage-upgrades`` from `ftw.upgrade <https://github.com/4teamwork/ftw.upgrade>`_.
So the first upgradesetp ``Upgrade ftw.referencewidget:default to 20181112105705: Fix registry field frontend edit`` must be installed via the ZMI under ``../portal_setup/manage_fullImport``. This sets the version for the package and so further upgrades can be installed via ``../@@manage-upgrades``.


Version 4.x
-----------
Version 4.x of ftw.referencewidget is only compatible with Plone 6 and Python 3.9 (maybe 3.7 and 3.8 as well).
It uses the module federation feature and boostrap 5 from Plone 6.


ContextSourceBinder
-------------------

With a `RelationeChoice` or `RelationList` of `RelationChoice` a source can be configured along with the field.
The `ContextSourceBinder` makes sure that only valid content can be selected.

By default, the source binder only checks for a valid portal_type when selecting content.

The default_filter implementation therefore looks like this:

.. code:: python

    def default_filter(source, value):
        """"
        Return ``True`` when the object is selectable, ``False``
        when it is not selectable.

        """"
        return value.portal_type in get_selectable_types_by_source(source)

Feel free to add your own filter method as source parameter in your field.
Example:

.. code:: python

    from ftw.referencewidget.filter import DefaultSelectable

    class CustomClass(DefaultSelectable):
        def is_selectable(self):
            return bool(..)
    ...

    directives.widget(realtionchoice_restricted_title=ReferenceWidgetFactory)
    realtionchoice_restricted_title = RelationChoice(
        title=_(u'Related Choice Restricted Title'),
        source=ReferenceObjSourceBinder(
            selectable_class=CustomClass),
        default=None,
        required=False,
    )

The `filter` takes two parameter the actual source object and a value, which is the content object.

Only `ReferenceObjSourceBinder` are supported. The SourceBinder takes the following parameters:

- selectable: Adds these types as selectable. Will act as complete configuration if `override` is set to True
- nonselectable: Adds these Types are not selectable. Will be ignored if `override` is set to True.
- allow_nonsearched_types: If this is set to true all the types will be traversable and selectable.
- override: Drops all global config and the base query if a list is passed to the widget. If this is set to true, `selectable` is not additive but acts as the complete configuration instead. `nonselectable` will be ignored.
- selectable_class: Custom ISelectable Class to determine if a content is selectable or not.

The parameters are same as for the widget (Backwards compatibility with 1.x releases).


Fields combinations (Registered converter)
------------------------------------------

The following combinations are supported:

- RelationList with value_type Relation --> Stores a List of RelationValues
- RelationList with value_type RelationChoice --> Stores a List of RelationValues
- Relation --> Stores a RelationValue
- List of RelationChoice --> Stores a list of absolute paths, without the portal root part
- TextLine --> Stores a absolute path as string, without the portal root part


TinyMCE Plone 5 - Internal Link widget replacement
--------------------------------------------------

With the version 3 of ftw.referencewidget within Plone 5.x the select2 internal link widget
automatically gets replaced by the ftw.referencewidget interna link browser.
Featering search and browsing within the referencebrowser popup. 


Links
-----

- Github: https://github.com/4teamwork/ftw.referencewidget
- Issues: https://github.com/4teamwork/ftw.referencewidget/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.referencewidget


Make restapi support NOT queries via @search endpoint
-----------------------------------------------------

.. code:: python

    def parse_complex_query(self, idx_query):
        idx_query = idx_query.copy()
        parsed_query = {}
        if "query" not in idx_query and "not" not in idx_query:
            raise QueryParsingError(
                "Query for index %r is missing a 'query' or 'not' key!" % self.index
            )
        if "query" in idx_query:
            qv = idx_query.pop("query")
            parsed_query["query"] = self.parse_simple_query(qv)
        if "not" in idx_query:
            nt = idx_query.pop("not")
            parsed_query["not"] = self.parse_simple_query(nt)

        for opt_key, opt_value in idx_query.items():
            if opt_key in self.query_options:
                opt_type = self.query_options[opt_key]
                try:
                    parsed_query[opt_key] = opt_type(opt_value)
                except ValueError:
                    raise QueryParsingError(
                        "Value %r for query option %r (index %r) could not be"
                        " casted to %r" % (opt_value, opt_key, self.index, opt_type)
                    )
            else:
                log.warning(
                    f"Unrecognized query option {opt_key!r} for index {self.index!r}"
                )
                # Pass along unknown option without modification
                parsed_query[opt_key] = opt_value

        return parsed_query


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.referencewidget`` is licensed under GNU General Public License, version 2.
