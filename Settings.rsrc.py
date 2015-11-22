{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':u'PyCraft Settings',
          'size':(534, 456),

         'components': [

{'type':'StaticText', 
    'name':'StaticText1', 
    'position':(9, 374), 
    'size':(500, -1), 
    'alignment':u'center', 
    'text':u'Mods are currently disabled.', 
    },

{'type':'List', 
    'name':'modList', 
    'position':(10, 166), 
    'size':(258, 195), 
    'enabled':False, 
    'items':[u'vanilla'], 
    },

{'type':'TextArea', 
    'name':'modData', 
    'position':(285, 126), 
    'size':(231, 172), 
    'enabled':False, 
    'text':u'Select a mod', 
    },

{'type':'Button', 
    'name':'saveIt', 
    'position':(281, 312), 
    'size':(238, 44), 
    'label':u'Apply', 
    },

{'type':'TextArea', 
    'name':'texdat', 
    'position':(284, 9), 
    'size':(231, 105), 
    'text':u'Select a texture', 
    },

{'type':'List', 
    'name':'texlist', 
    'position':(11, 10), 
    'size':(257, 144), 
    'items':[], 
    },

] # end components
} # end background
] # end backgrounds
} }
