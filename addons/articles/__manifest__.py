# -*- coding: utf-8 -*-
{
    'name': "Articles",

    'summary': """
        Decompsed articles.""",

    'description': """
        Decompsed articles.
    """,

    'author': "Danny",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'SLR',
    'version': '13.0.0.2',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'framework_overrides'
    ],

    # always loaded
    'data': [
        'security/security_groups.xml',

        'security/ir.model.access.csv',

        'views/corpus/article_ranking.xml',
        'views/corpus/corpus_article.xml',
        'views/corpus/corpus.xml',
        'views/corpus/journal.xml',
        'views/corpus/load_failure.xml',
        'views/corpus/year.xml',

        'views/prototype/prototype_article.xml',
        'views/prototype/topic.xml',

        'views/vocabulary/stem.xml',
        'views/vocabulary/word.xml',

        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
