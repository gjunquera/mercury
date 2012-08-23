// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.BroadcastResponse;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.ProviderResponse;
import com.mwr.mercury.Message.Response;
import com.mwr.mercury.Session;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ServiceInfo;
import android.util.Base64;

import java.util.List;

public class Broadcast
{
	public static void info(List<KVPair> argsArray,
			Session currentSession)
	{
		//Assign filter and permissions if they came in the arguments
		String filter = Common.getParamString2(argsArray, "filter");
		String permissions = Common.getParamString2(argsArray, "permissions");
				
		//Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext.getPackageManager();
		List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_RECEIVERS | PackageManager.GET_PERMISSIONS);
		
		Response.Builder responseBuilder = Response.newBuilder();
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
						BroadcastResponse.Info.Builder infoBuilder = BroadcastResponse.Info.newBuilder();
						infoBuilder.setPackageName(receivers[i].packageName);
						infoBuilder.setReceiver(receivers[i].name);
						if (receivers[i].permission == null) 
							infoBuilder.setPermission("null");							
						else
							infoBuilder.setPermission(receivers[i].permission);
				    	responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
						broadcastBuilder.addInfo(infoBuilder);
					}
				}
			}
		}
		
		Response response = Response.newBuilder().setData(broadcastBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(response.toByteArray(), Base64.DEFAULT), false);
	}

	public static void send(List<KVPair> argsArray,
			Session currentSession)
	{
		// Parse intent
		Intent intent = Common.parseIntentGeneric2(argsArray, new Intent());

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
    	currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false);
	}

}
