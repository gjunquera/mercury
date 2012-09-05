// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.BroadcastResponse;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.Response;
import com.mwr.mercury.Session;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.res.AssetManager;
import android.content.res.XmlResourceParser;
import android.util.Base64;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;

public class Broadcast
{
	public static void info(List<KVPair> argsArray,
			Session currentSession)
	{
		//Assign filter and permissions if they came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		String permissions = Common.getParamString(argsArray, "permissions");
				
		//Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext.getPackageManager();
		List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_RECEIVERS | PackageManager.GET_PERMISSIONS);
		
		Response.Builder responseBuilder = Response.newBuilder();
    	responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		BroadcastResponse.Builder broadcastBuilder = BroadcastResponse.newBuilder();
		//Iterate through packages
		for (PackageInfo package_:packages)
		{
			ActivityInfo[] receivers = package_.receivers;			
			
			if (receivers != null)
			{	
				for (int i = 0; i < receivers.length; i++)
				{							
					boolean relevantFilter = false;
					boolean relevantPermissions = false;
					boolean noFilters = false;
					boolean bothFiltersRelevant = false;
					
					//Check if a filter was used
					if (filter.length() > 0)
						relevantFilter = package_.packageName.toUpperCase().contains(filter.toUpperCase()) || receivers[i].name.toUpperCase().contains(filter.toUpperCase());
					
					//Check if a permission filter was used
					try
					{
						if (permissions.length() > 0)
						{
							if (permissions.toUpperCase().equals("NULL"))
								relevantPermissions = (receivers[i].permission == null);
							else
								relevantPermissions = receivers[i].permission.toUpperCase().contains(permissions.toUpperCase());
						}
					} catch (Throwable t) {}
					
					//Check if no parameters were given
					if (filter.length() == 0 && permissions.length() == 0)
						noFilters = true;
					
					boolean bothFiltersPresent = false;
					if ((filter != "") && (permissions != ""))
						bothFiltersPresent = true;
					
					if (bothFiltersPresent && relevantFilter && relevantPermissions)
						bothFiltersRelevant = true;
					
					//Apply filter and only look @ exported providers
					if (((bothFiltersPresent && bothFiltersRelevant) || (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters)) && receivers[i].exported)
					{
						List<String> actions = findReceiverActions(currentSession, receivers[i]);
						
						BroadcastResponse.Info.Builder infoBuilder = BroadcastResponse.Info.newBuilder();
						for (String action: actions)
							infoBuilder.addAction(action);
						infoBuilder.setPackageName(receivers[i].packageName);
						infoBuilder.setReceiver(receivers[i].name);
						if (receivers[i].permission == null) 
							infoBuilder.setPermission("null");							
						else
							infoBuilder.setPermission(receivers[i].permission);
						broadcastBuilder.addInfo(infoBuilder);
					}
				}
			}
		}
		
		Response response = responseBuilder.setData(broadcastBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(response.toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void send(List<KVPair> argsArray,
			Session currentSession)
	{
		// Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());

		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
			currentSession.applicationContext.sendBroadcast(intent);
			responseBuilder.addStructuredData(Common.createKVPair("intent", intent.toString()));
	    	responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		}
		catch (Throwable t)
		{
	    	responseBuilder.setError(ByteString.copyFrom(t.getMessage().getBytes()));
		}
    	currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}
	
	// Added in order to get the actions of each broadcast receiver
	// Change added by Luander Ribeiro <luander.r@samsung.com>
	// in Aug 27 - 2012
	/**
	 * Get a list of actions of a given receiver
	 * @param currentSession the session for current request
	 * @param receivers An ActivityInfo with a receiver information
	 * @return A list of strings containing the actions of a receiver or an empty list, if there is no action
	 */
	private static List<String> findReceiverActions(Session currentSession, ActivityInfo receivers)
	{
		List<String> actions = new ArrayList<String>();
		try
		{
			AssetManager am = currentSession.applicationContext.createPackageContext(receivers.packageName, 0).getAssets();
			XmlResourceParser xml = am.openXmlResourceParser("AndroidManifest.xml");

			//XML parsing
			while (xml.next() != XmlPullParser.END_DOCUMENT) {
				switch (xml.getEventType()) {
				case XmlPullParser.START_TAG:
					// Find receiver tag to start looking for intent filters
					if ("receiver".equals(xml.getName()))
					{
						String receiverName = searchXmlAttr(xml, "android:name");
						if (receiverName.length() == 0)
						{
							receiverName = searchXmlAttr(xml, "name");
						}
						// If the tag name matches with receiver, search for its intent filters
						if (receiverName.length() > 0 &&
								receivers.name.endsWith(receiverName))
						{
							//iterate until receiver END_TAG
							while(xml.next() != XmlPullParser.END_TAG) {
								if (xml.getEventType() == XmlPullParser.START_TAG &&
										"intent-filter".equals(xml.getName()))
								{
									//iterate until intent-filter END_TAG
									while(xml.next() != XmlPullParser.END_TAG) {
										if (xml.getEventType() == XmlPullParser.START_TAG &&
												"action".equals(xml.getName()))
										{
											String action = searchXmlAttr(xml, "android:name");
											if (action.length() == 0)
												action = searchXmlAttr(xml, "name");
											if (action.length() > 0)
												actions.add(action);
											//iterate until action END_TAG
											while(xml.next() != XmlPullParser.END_TAG);										
										}
									} 
								}
							}
						}
					}
					break;
				case XmlPullParser.END_TAG:
					break;
				case XmlPullParser.TEXT:
					break;
				default:
					break;
				}
			}
		}
		catch (NameNotFoundException e){}
		catch (IOException e){}
		catch (XmlPullParserException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return actions;
	}
	
	//Searches for an attribute in "XML tag"
	private static String searchXmlAttr(XmlResourceParser xml, String attrName) 
	{
		for (int j = 0; j < xml.getAttributeCount(); j++)
		{
			String name = xml.getAttributeName(j);
			String value = xml.getAttributeValue(j);
			// If the tag name matches with receiver, search for its intent filters
			if (attrName.equals(name)) 
			{
				return value;
			}
		}
		return "";
	}

}
