// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.ActivityResponse;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.Response;
import com.mwr.mercury.Session;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.util.Base64;

import java.util.List;

public class Activity
{
	public static void info(List<KVPair> argsArray,
			Session currentSession)
	{
		//Assign filter if one came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		
		//Iterate through all packages
		List<PackageInfo> packages = currentSession.applicationContext.getPackageManager().getInstalledPackages(0);
		Response.Builder responseBuilder = Response.newBuilder();
		
		ActivityResponse.Builder activityBuilder = ActivityResponse.newBuilder();
        for(PackageInfo pack : packages)
        {
        	//Get activities in package
            ActivityInfo[] activities = null;
            try
            {
            	activities = currentSession.applicationContext.getPackageManager().getPackageInfo(pack.packageName, PackageManager.GET_ACTIVITIES).activities;
            }
            catch (Exception e) {
            	responseBuilder.setError(ByteString.copyFrom(Common.ERROR_UNKNOWN.getBytes()));
            }
            
        	if (activities != null)
			{	
				for (int i = 0; i < activities.length; i++)
				{
					if (activities[i].exported == true)
					{
						boolean filterPresent = filter.length() != 0;
						boolean filterRelevant = pack.packageName.toUpperCase().contains(filter.toUpperCase()) || activities[i].name.toUpperCase().contains(filter.toUpperCase());
						
						if ((filterPresent && filterRelevant) || !filterPresent)
						{	
							ActivityResponse.Info.Builder infoBuilder = ActivityResponse.Info.newBuilder();
							infoBuilder.setPackageName(activities[i].packageName);
							infoBuilder.setActivity(activities[i].name);
							activityBuilder.addInfo(infoBuilder);
						}
					}
				}
            	responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
			}
        }
		Response response = Response.newBuilder().setData(activityBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(response.toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void start(List<KVPair> argsArray,
			Session currentSession)
	{
		//Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
		
		Response.Builder responseBuilder = Response.newBuilder();
		try	{
			currentSession.applicationContext.startActivity(intent);
			responseBuilder.addStructuredData(Common.createKVPair("intent", intent.toString()));
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		}
		catch (Throwable t)
		{
			responseBuilder.setError(ByteString.copyFrom(t.getMessage().getBytes()));
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void match(List<KVPair> argsArray,
			Session currentSession)
	{
		//Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
		
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
		
			//Get all activities and iterate through them
			List<ResolveInfo> activities = currentSession.applicationContext.getPackageManager().queryIntentActivities(intent, PackageManager.MATCH_DEFAULT_ONLY & PackageManager.GET_ACTIVITIES & PackageManager.GET_INTENT_FILTERS & PackageManager.GET_RESOLVED_FILTER	);
			
			String returnVal = intent.toString();
			
			for (int i = 0; i < activities.size(); i++)
			{

				String activityPackage = activities.get(i).activityInfo.packageName;
				String activityTargetActivity = activities.get(i).activityInfo.name;
				
				responseBuilder.addStructuredData(Common.createKVPair("package_name", activityPackage));
				responseBuilder.addStructuredData(Common.createKVPair("activity", activityTargetActivity));
			}
			responseBuilder.setData(ByteString.copyFrom(returnVal.trim().getBytes()));
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		}
		catch (Exception e)
		{
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_UNKNOWN.getBytes()));
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void launchIntent(List<KVPair> argsArray,
			Session currentSession)
	{
		//Assign filter if one came in the arguments
		String packageName = Common.getParamString(argsArray, "packageName");
		
		Intent intent = currentSession.applicationContext.getPackageManager().getLaunchIntentForPackage(packageName);
		
		Response.Builder responseBuilder = Response.newBuilder();
		//Send intent back
		if (intent != null)
		{
			responseBuilder.setData(ByteString.copyFrom(intent.toString().getBytes()));
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		}
		else
		{
			responseBuilder.setData(ByteString.copyFrom("No intent returned".getBytes()));
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_UNKNOWN.getBytes()));
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

}
