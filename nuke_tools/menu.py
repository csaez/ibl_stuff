# GUI mode, setup the menus
myToolbar = nuke.toolbar( 'Nodes' )
myMenu = myToolbar.addMenu( 'IBLstuff', icon='IBLstuff.png' )
myMenu.addCommand( "IBLrebuild", "nuke.createNode( 'IBLrebuild' )", icon="IBLrebuild.png" )
myMenu.addCommand( "IBLcalibrate", "nuke.createNode( 'IBLcalibrate')", icon="IBLcalibrate.png" )