#!/usr/bin/env python
#
#

import pyjsonrpc
import os.path

import sys
import xml.etree.ElementTree

http_client = pyjsonrpc.HttpClient(
	url = "http://localhost:8080/jsonrpc",
	username = "kodi",
	password = "kodi"
)

shows =  http_client.call("VideoLibrary.GetTVShows")

def readNFO(filename):
    tree = xml.etree.ElementTree.parse(filename)
    root = tree.getroot()
    plotelement = root.find("title")
    if( plotelement != None ):
	nfodata = plotelement.text
	details =  http_client.call("VideoLibrary.GetEpisodeDetails",
		episodeid=episodeid, properties=['title', 'file'] )
	kodidata = details[u'episodedetails'][u'title']
#print "Title: nfo %s kodi %s " %( nfodata, kodidata)
	if( nfodata == None) and (len(kodidata) == 0):
	    print "Should download new nfo file for", filename
	if( nfodata != kodidata ):
	    if (nfodata != None) and (len(kodidata) == 0):
		print "Set title to:", nfodata
#		http_client.call("VideoLibrary.SetEpisodeDetails",
#			episodeid=episodeid, title=nfodata)

    plotelement = root.find("plot")
    if( plotelement != None ):
	nfodata = plotelement.text
	details =  http_client.call("VideoLibrary.GetEpisodeDetails",
		episodeid=episodeid, properties=['plot', 'file'] )
	kodidata = details[u'episodedetails'][u'plot']
	if( nfodata == None) and (len(kodidata) == 0):
	    print "Should download new nfo file for", filename
	if( nfodata != kodidata ):
	    if (nfodata != None) and (len(kodidata) == 0):
		print "Set plot to:", nfodata
		http_client.call("VideoLibrary.SetEpisodeDetails",
			episodeid=episodeid, plot=nfodata)


def handelEpisode(episodeid):
    details =  http_client.call("VideoLibrary.GetEpisodeDetails",
	    episodeid=episodeid, properties=['plot', 'file'] )
    videofile =  details[u'episodedetails'][u'file']
    if os.path.isfile(videofile):
	(base, ext) = os.path.splitext(videofile)
	nfofile = base + ".nfo"
	if os.path.isfile( nfofile ):
#	    print "   nfo", nfofile
	    readNFO(nfofile)
	else:
	    print "no nfo", videofile
    else:
	print "ERROR!", videofile
	http_client.call("VideoLibrary.RemoveEpisode", episodeid)

for show in shows[u'tvshows']:
    print show
    episodes =  http_client.call("VideoLibrary.GetEpisodes", show[u'tvshowid'])
#    print episodes
    if u'episodes' in episodes:
	for episode in episodes[u'episodes']:
	    episodeid = episode[u'episodeid']
	    handelEpisode(episodeid)

		
