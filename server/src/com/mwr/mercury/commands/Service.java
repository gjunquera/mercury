// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.google.protobuf.ByteString;
import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.Response;
import com.mwr.mercury.Message.Response.Builder;
import com.mwr.mercury.Message.ServiceResponse;
import com.mwr.mercury.Session;
import com.mwr.mercury.Message.ProviderResponse;

import android.content.ComponentName;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ServiceInfo;
import android.util.Base64;

import java.util.List;

public class Service
{
	public static void info(List<KVPair> argsArray, Session currentSession){
		//Assign filter and permissions if they came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		String permissions = Common.getParamString(argsArray, "permissions");
				
		//Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext.getPackageManager();
		List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_SERVICES | PackageManager.GET_PERMISSIONS);
		
		ServiceResponse.Builder serviceBuilder = ServiceResponse.newBuilder();
		//Iterate through packages
		for (PackageInfo package_:packages)
		{
			ServiceInfo[] services = package_.services;			
			
			if (services != null)
			{	
				for (int i = 0; i < services.length; i++)
				{							
					boolean relevantFilter = false;
					boolean relevantPermissions = false;
					boolean noFilters = false;
					boolean bothFiltersRelevant = false;
					
					//Check if a filter was used
					if (filter.length() > 0)
						relevantFilter = package_.packageName.toUpperCase().contains(filter.toUpperCase()) || services[i].name.toUpperCase().contains(filter.toUpperCase());
					
					//Check if a permission filter was used
					try
					{
						if (permissions.length() > 0)
						{
							if (permissions.toUpperCase().equals("NULL"))
								relevantPermissions = (services[i].permission == null);
							else
								relevantPermissions = services[i].permission.toUpperCase().contains(permissions.toUpperCase());
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
					if (((bothFiltersPresent && bothFiltersRelevant) || (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters)) && services[i].exported)
					{
						ServiceResponse.Info.Builder infoBuilder = ServiceResponse.Info.newBuilder();
						infoBuilder.setPackageName(services[i].packageName);
						infoBuilder.setService(services[i].name);
						//To avoid NullPointerException
						String permission = "" + services[i].permission;
						infoBuilder.setPermission(permission);
						serviceBuilder.addInfo(infoBuilder);
					}
				}
			}
		}
		Response.Builder responseBuilder = Response.newBuilder();
		responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		responseBuilder.setData(serviceBuilder.build().toByteString());
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}
	
	public static void start(List<KVPair> argsArray, Session currentSession){
		//Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
			ComponentName service = currentSession.applicationContext.startService(intent);
			if (service != null) {
				responseBuilder.addStructuredData(Common.createKVPair("intent", intent.toString()));
				responseBuilder.addStructuredData(Common.createKVPair("package_and_class", service.flattenToString()));
				responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
			} else {
				responseBuilder.setError(ByteString.copyFrom("Start service failed".getBytes()));				
			}
//			currentSession.sendFullTransmission("Service started with " + intent.toString() + " - " + service.flattenToString(), "");
		}
		catch (Throwable t)
		{
			responseBuilder.setError(ByteString.copyFrom(t.getMessage().getBytes()));
//			currentSession.sendFullTransmission("", t.getMessage());
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}
	
	public static void stop(List<KVPair> argsArray, Session currentSession){
		//Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
		
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
			boolean stopped = currentSession.applicationContext.stopService(intent);
			if (stopped)
			{
				responseBuilder.addStructuredData(Common.createKVPair("intent", intent.toString()));
				responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
//				currentSession.sendFullTransmission("Service stopped with " + intent.toString(), "");
			}
			else
				responseBuilder.setError(ByteString.copyFrom("Stopping service failed".getBytes()));
//				currentSession.sendFullTransmission("Stopping service failed", "");
		}
		catch (Throwable t)
		{
			responseBuilder.setError(ByteString.copyFrom(t.getMessage().getBytes()));
//			currentSession.sendFullTransmission("", t.getMessage());
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

}
