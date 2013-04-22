# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  
@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    #table=plugin_jqgrid(db.Upload,columns=['Name','Type_of_song','artist','album'],col_widths=
    #   {'Name':160,'Type_of_song':25,'artist':120,'album':120,'file':120},width=775,height=300)
    table=plugin_jqgrid(db.Upload,columns=['id','Type_of_song','Name','album','artist','upload_a_song'],col_widths=
     {'id':30,'Name':180,'album':160,'artist':160,'Type_of_song':20,'upload_a_song':100},width=640,height=220)
    #This specifies the various coloums that one wants to show in the front page using yhe plugin jggrid
    #all the song will be displayed in the playlist giving the details of various song,along with the optio to download it.
    type_song=db(db.Types_of_songs.id>0).select(orderby = db.Types_of_songs.song_type)
    #This allows the user to view songs of a particular gener  
    return dict(type_song=type_song,table=table)

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@auth.requires_login()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()




######################################################################################################
#def Types_of_songs():
   #table=plugin_jqgrid(db.Upload,columns=[],col_widths=
   #  {'id':80,'name':160,'movie_album':130,'singer':120,'genre':120,'year':100,'file':120},width=803,height=395)
#   table=plugin_jqgrid(db.Upload,columns=['Name','Type_of_song','artist','album'],col_widths=
#     {'Name':160,'Type_of_song':100,'artist':120,'album':120,'file':120},width=775,height=300)
#   type_song=db(db.Types_of_songs.id>0).select()
#   form=SQLFORM(db.Upload,fields=['upload_a_song','Type_of_song','Name','artist','album'])
#   if form.accepts(request.vars,session):
#      response.flash='Song has been uploaded'
#  return dict(type_song=type_song,form=form,table=table)
#######################################################################################################
@auth.requires_membership('Super_user')
def admin():
    return dict()

@auth.requires_membership('Super_user')
def admin_remove_user():
    user_list=db(db.auth_user.id>0).select()
    return dict(user_list=user_list)

@auth.requires_membership('Super_user')
def delete_user():
    db(db.auth_user.id==request.args(0)).delete()
    redirect(URL(r=request,f='admin_remove_user'))

@auth.requires_membership('Super_user')    
def admin_remove_song():
    song=db(db.Upload.id>0).select(orderby=~db.Upload.Upload_on)
    return dict(songs=song)

@auth.requires_membership('Super_user')
def delete_song():
    db(db.Upload.id==request.args(0)).delete()
    redirect(URL(r=request,f='admin_remove_song'))

@auth.requires_membership('Super_user')    
def admin_remove_comments():
    comments=db(db.Comments.id>0).select(orderby=~db.Comments.Commented_on)
    return dict(comments=comments)

@auth.requires_membership('Super_user')
def delete_comment():
    db(db.Comments.id==request.args(0)).delete()
    redirect(URL(r=request,f='admin_remove_comments'))

@auth.requires_membership('Super_user')
def admin_add_gener():
    form=SQLFORM(db.Types_of_songs,fields=['song_type'])
    if form.accepts(request.vars,session):
      response.flash='Gener Added'
    return dict(form=form)
      
@auth.requires_login()  
def upload():
   form=SQLFORM(db.Upload,fields=['upload_a_song','Type_of_song','Name','artist','album'])
   # create a form in which the user can upload a song .It askes for various details like album,gener etc,while uploading
   if form.accepts(request.vars,session):
      response.flash='Song has been Uploaded'
      redirect(URL(r=request,f='index'))#This redirects the user to the index page once the song has uploaded   
   return dict(form=form)

@auth.requires_login()
def view_songs():
   #view=[]
   #db().update(view[Upload.id]=Upload.id+1)
   return dict(songs=db(db.Upload.Type_of_song==request.args(0)).select(orderby=~db.Upload.Upload_on))
   #Shows the list of all the songs of a particular gener

@auth.requires_login()
def song_details():
   #db.Rating.Name_song.default=request.args(1)
   song=db(db.Upload.id==request.args(0)).select()#"song" contains the name of the selected song which is passed as an argument 
   download=db(db.Upload.upload_a_song==request.args(0)).select()#allows user to download the song
   comments=db(db.Comments.Name==request.args(0)).select(orderby=~db.Comments.Commented_on)#shows the previous comments to th song
   rating=db(db.Rating.Name==request.args(0)).select()
########################
   
#   y=request.args(0)
   Countx=db(db.Views.gana==request.args(0)).select()
   #print Countx
   #################################################  
   return dict(song=song,comments=comments,download=download,rating=rating,Count=Countx)
   #return dict(song=song,counter=session.counter,download=download)

@auth.requires_login()
def add_comment():
   db.Comments.Nick_name.default = auth.user.first_name#sets "nick name "as the first name of the logged in user
   db.Comments.Name.default=request.args(0)#sets "Name" as the id of the song selected
   db.Comments.NAME_song.default=request.args(1)
   form=SQLFORM(db.Comments,fields=['comment'])#creates a  form in which comment can be given
   if form.accepts(request.vars,session):
      response.flash='Thanks for your Comments'
      redirect(URL(r=request,f='index'))#This redirects the user to the index page once the song has uploaded 
   return dict(form=form)

#def playlist():
#    db.Playlist.song.default=auth.user.id
#    db.Playlist.
@auth.requires_login()    
def player():
    
    db.Views.insert(gana=request.args(1),Name=request.args(2))
    songs=db(db.Views.gana==request.args(1)).select()[0]
    Count=songs.view #song=db(db.Rating.Name==request.args(1)).select()[0] 
    db(db.Views.gana==request.args(1)).update(view=Count+1)
    songs=db(db.Views.gana==request.args(1)).select()[0]
    Count=songs.view
    #print Count
    file_name=URL('download',args=request.args(0))#for using the audio tag to play a song from the selected gener 
    return dict(file_name=file_name)

@auth.requires_login()
def playlist():
    #print auth.user.id
    db.Playlist.insert(user_id=auth.user.id,song=request.args(0),Name=request.args(1))
    #print request.args(1)
    #db.Playlist.Name.default=request.args(1)
    redirect(URL(r=request,f='View_playlist'))

@auth.requires_login()    
def View_playlist():
    return dict(songs=db(db.Playlist.user_id==auth.user.id).select())

@auth.requires_login()
def delete_playlist():
    db(db.Playlist.id==request.args(0)).delete()
    redirect(URL(r=request,f='View_playlist'))

@auth.requires_login()
def rate():
    form=SQLFORM(db.Rating,fields=['Rate'])#creates a  form in which comment can be given
    if form.accepts(request.vars,session):
      response.flash='Thanks for rating this song'
      redirect(URL(r=request,f='index'))
##############################################
@auth.requires_login()
def rating():
     rate=int(request.args(0))
     #y=request.args(1)
     db.Rating.insert(Name=request.args(1),Name_song=request.args(2))
     print request.args(2)
     
     
     song=db(db.Rating.Name==request.args(1)).select()[0]   
      
     Count=song.Times_played
     Sum=song.Sum
     db(db.Rating.Name==request.args(1)).update(Times_played=Count+1)
     db(db.Rating.Name==request.args(1)).update(Sum=Sum+rate)
     song=db(db.Rating.Name==request.args(1)).select()[0]
     
     Count=song.Times_played
     Sum=song.Sum
     
     div=Sum/Count
     
     db(db.Rating.Name==request.args(1)).update(Rate=div) 
#     print 'c_new=',c
 #    print 's_new=',s
  #   print div
   #  print 'refresh'
     redirect(URL(r=request,f='index'))
     return dict()
################################################
@auth.requires_login()
def top_10():
     song_10=db().select(db.Rating.ALL,orderby=~db.Rating.Rate)
     #Count=0  
     #print song_10[3].Name
     return dict (song_10 = song_10)

@auth.requires_login()   
def top_played():
     song_played=db().select(db.Views.ALL,orderby=~db.Views.view)
     return dict (song_played = song_played)

@auth.requires_login()   
def recently_added():
     recent=db().select(db.Upload.ALL,orderby=~db.Upload.Upload_on)
     return dict ( recent = recent)
