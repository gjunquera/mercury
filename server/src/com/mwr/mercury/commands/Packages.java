// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.PackageResponse;
import com.mwr.mercury.Message.Response;
import com.mwr.mercury.Session;

import android.content.pm.ActivityInfo;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.pm.ProviderInfo;
import android.content.pm.ServiceInfo;
import android.content.res.AssetManager;
import android.content.res.XmlResourceParser;
import android.util.Base64;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.xmlpull.v1.XmlPullParser;

public class Packages
{
	public static void info(List<KVPair> argsArray,
			Session currentSession)
	{

		// Assign filter and permissions if they came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		String permissions = Common.getParamString(argsArray, "permissions");

		// Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext
				.getPackageManager();
		List<PackageInfo> packages = pm
				.getInstalledPackages(PackageManager.GET_PERMISSIONS
						| PackageManager.GET_CONFIGURATIONS
						| PackageManager.GET_GIDS
						| PackageManager.GET_SHARED_LIBRARY_FILES);

		PackageResponse.Builder packageBuilder = PackageResponse.newBuilder();
		// Iterate through packages
		try {
			for (PackageInfo currentPackage : packages)
			{
				ApplicationInfo app = currentPackage.applicationInfo;
	
				String packageName = app.packageName;
				String processName = app.processName;
				String dataDir = app.dataDir;
				String publicSourceDir = app.publicSourceDir;
				Integer uid = app.uid;
				String sharedUserId = currentPackage.sharedUserId;
				int[] gids = currentPackage.gids;
				String version = currentPackage.versionName;
				String[] libraries = app.sharedLibraryFiles;
	
				// Find all permissions that this app has requested
				String requestedPermissions = "";
				String[] requestedPermissionsArray = currentPackage.requestedPermissions;
	
				String librariesString = "";
				if (libraries != null)
					for (int i = 0; i < libraries.length; i++)
						librariesString += libraries[i] + "; ";
	
				// Get the GIDs
				String gidString = "";
				if (gids != null)
					for (int z = 0; z < gids.length; z++)
						gidString += new Integer(gids[z]).toString() + "; ";
	
				boolean relevantFilter = filter != "";
				if (relevantFilter)
					relevantFilter = packageName.toUpperCase().contains(
							filter.toUpperCase())
							|| processName.toUpperCase().contains(
									filter.toUpperCase())
							|| dataDir.toUpperCase().contains(filter.toUpperCase())
							|| publicSourceDir.toUpperCase().contains(
									filter.toUpperCase())
							|| (uid.toString().equals(filter));
	
				boolean relevantPermissions = permissions != "";
				if (relevantPermissions)
					relevantPermissions = requestedPermissions.toUpperCase()
							.contains(permissions.toUpperCase());
	
				boolean bothFiltersPresent = false;
				if ((filter != "") && (permissions != ""))
					bothFiltersPresent = true;
	
				boolean bothFiltersRelevant = false;
				if (bothFiltersPresent && relevantFilter && relevantPermissions)
					bothFiltersRelevant = true;
	
				boolean noFilters = (filter.length() == 0)
						&& (permissions.length() == 0);
	
				// Apply filter
				if ((bothFiltersPresent && bothFiltersRelevant)
						|| (!bothFiltersPresent && (relevantFilter || relevantPermissions))
						|| (!bothFiltersPresent && noFilters))
				{
					PackageResponse.Info.Builder infoBuilder = PackageResponse.Info.newBuilder();
					infoBuilder.setPackageName(packageName);
					infoBuilder.setProcessName(processName);
					if (version != null)
						infoBuilder.setVersion(version);
					else 
						infoBuilder.setVersion("No version info");
					infoBuilder.setDataDirectory(dataDir);
					infoBuilder.setApkPath(publicSourceDir);
					infoBuilder.setUid(uid);
					// Get the GIDs
					if (gids != null)
						for (int z = 0; z < gids.length; z++)
							infoBuilder.addGuid(gids[z]);
	
					if (libraries != null)
						for (int i = 0; i < libraries.length; i++)
							infoBuilder.addSharedLibraries(libraries[i]);
	
					if (sharedUserId != null)
						infoBuilder.setSharedUserId(sharedUserId);
					
					if (requestedPermissionsArray != null)
						for (String permission : requestedPermissionsArray)
							infoBuilder.addPermission(permission);
					getSecretCodes(packageName, infoBuilder, currentSession);
					packageBuilder.addInfo(infoBuilder);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		Response response = Response.newBuilder().setData(packageBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(response.toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void sharedUid(List<KVPair> argsArray,
			Session currentSession)
	{
		PackageResponse.Builder packageBuilder = PackageResponse.newBuilder();

		// Get all the parameters
		String filter = Common.getParamString(argsArray, "uid");

		// Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext
				.getPackageManager();
		List<PackageInfo> packages = pm
				.getInstalledPackages(PackageManager.GET_PERMISSIONS);

		List<Integer> uidList = new ArrayList<Integer>();

		// Get all UIDs
		for (PackageInfo package_ : packages)
		{
			ApplicationInfo app = package_.applicationInfo;

			if (!uidList.contains(app.uid))
				uidList.add(app.uid);
		}

		// Iterate through packages
		for (Integer uid : uidList)
		{
			String[] packageNames = pm.getPackagesForUid(uid);
			List<String> accumulatedPermissions = new ArrayList<String>();

			if ((filter.length() > 0 && filter.equals(uid.toString()))
					|| filter.length() == 0)
			{
				PackageResponse.SharedUid.Builder sharedUidBuilder = PackageResponse.SharedUid.newBuilder();
				sharedUidBuilder.setUid(uid);
				
				if (packages != null)
				{
					for (int s = 0; s < packageNames.length; s++)
					{
						// Get package permissions and add to list of
						// accumulated
						PackageInfo pack = null;

						try
						{
							pack = currentSession.applicationContext
									.getPackageManager().getPackageInfo(
											packageNames[s],
											PackageManager.GET_PERMISSIONS);
						}
						catch (Exception e)
						{
						}

						String[] requestedPermissionsArray = pack.requestedPermissions;

						if (requestedPermissionsArray != null)
						{
							for (String permission : requestedPermissionsArray)
								if (!accumulatedPermissions
										.contains(permission))
									accumulatedPermissions.add(permission);// += permission + "; ";
						}
						sharedUidBuilder.addPackageNames(packageNames[s]);
					}

				}
				// Send accumulated permissions
				sharedUidBuilder.addAllPermissions(accumulatedPermissions);
				packageBuilder.addSharedUid(sharedUidBuilder);
			}
		}

		Response response = Response.newBuilder().setData(packageBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(response.toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void attackSurface(List<KVPair> argsArray,
			Session currentSession)
	{
		// Get all the parameters
		String packageName = Common.getParamString(argsArray, "filter");
		Response.Builder responseBuilder = Response.newBuilder();
		PackageResponse.Builder packageBuilder = PackageResponse.newBuilder();
		
		// Get all packages from packagemanager
		List<String> packageNames = new ArrayList<String>();
		if (packageName == null || (packageName.length() == 0))
		{
			// Get all packages from packagemanager
			PackageManager pm = currentSession.applicationContext
					.getPackageManager();
			List<PackageInfo> packages = pm
					.getInstalledPackages(PackageManager.GET_CONFIGURATIONS);
			for (PackageInfo pkg : packages)
				packageNames.add(pkg.packageName);
		}
		else
		{
			// Add just original package if not wildcard
			packageNames.add(packageName);
		}
		
		try
		{
			for (String pkgName : packageNames)
			{
				// Check number of exported activities
				int numActivities = 0;
	
				ActivityInfo[] activities = currentSession.applicationContext
							.getPackageManager().getPackageInfo(pkgName,
								PackageManager.GET_ACTIVITIES).activities;
				if (activities != null)
					for (int i = 0; i < activities.length; i++)
						if (activities[i].exported)
							numActivities++;
	
				// Check number of exported receivers
				int numReceivers = 0;
				ActivityInfo[] receivers = currentSession.applicationContext
							.getPackageManager().getPackageInfo(pkgName,
								PackageManager.GET_RECEIVERS).receivers;
				if (receivers != null)
					for (int i = 0; i < receivers.length; i++)
						if (receivers[i].exported)
							numReceivers++;
	
				// Check number of exported providers
				int numProviders = 0;
				ProviderInfo[] providers = currentSession.applicationContext
							.getPackageManager().getPackageInfo(pkgName,
								PackageManager.GET_PROVIDERS).providers;
				if (providers != null)
					for (int i = 0; i < providers.length; i++)
						if (providers[i].exported)
							numProviders++;
	
				// Check number of exported services
				int numServices = 0;
				ServiceInfo[] services = currentSession.applicationContext
							.getPackageManager().getPackageInfo(pkgName,
								PackageManager.GET_SERVICES).services;
				if (services != null)
					for (int i = 0; i < services.length; i++)
						if (services[i].exported)
							numServices++;
	
					PackageResponse.AttackSurface.Builder attackSurfaceBuilder = PackageResponse.AttackSurface.newBuilder();
					attackSurfaceBuilder.setPackageName(pkgName);
					attackSurfaceBuilder.setActivities(numActivities);
					attackSurfaceBuilder.setReceivers(numReceivers);
					attackSurfaceBuilder.setProviders(numProviders);
					attackSurfaceBuilder.setServices(numServices);
	
				if ((currentSession.applicationContext.getPackageManager()
							.getPackageInfo(pkgName, 0).applicationInfo.flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0)
						attackSurfaceBuilder.setDebuggable(true);
					else
						attackSurfaceBuilder.setDebuggable(false);
	
				String shared = currentSession.applicationContext
							.getPackageManager().getPackageInfo(pkgName, 0).sharedUserId;
	
				if (shared != null)
				{
					attackSurfaceBuilder.setSharedUserId(shared);
				}
				packageBuilder.addAttackSurface(attackSurfaceBuilder);
			}
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		} catch (Throwable t)
		{
			responseBuilder.setError(ByteString.copyFrom(t.getMessage().getBytes()));
		}
		
		Response response = responseBuilder.setData(packageBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(response.toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void path(List<KVPair> argsArray,
			Session currentSession)
	{
		String packageName = Common.getParamString(argsArray, "packageName");

		Response.Builder responseBuilder = Response.newBuilder();
		List<String> pathList = new ArrayList<String>();
		// Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext
				.getPackageManager();
		List<PackageInfo> packages = pm
				.getInstalledPackages(PackageManager.GET_PERMISSIONS
						| PackageManager.GET_CONFIGURATIONS
						| PackageManager.GET_GIDS);

		String packagePath = "";

		// Iterate through packages
		for (PackageInfo package_ : packages)
		{
			ApplicationInfo app = package_.applicationInfo;

			// Check for package name
			if (app.packageName.equals(packageName))
			{
				packagePath = app.publicSourceDir;
				pathList.add(app.publicSourceDir);
				break;
			}
		}

		// Check if an odex file exists for the package
		if (new File(packagePath.replace(".apk", ".odex")).exists())
			pathList.add(packagePath.replace(".apk", ".odex"));

		// Send to client
		responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		responseBuilder.addStructuredData(Common.createKVPair("path", pathList));
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);		
	}
	
	private static void getSecretCodes(String packageName, PackageResponse.Info.Builder info, Session currentSession) 
	{
		
		// Get all packages from packagemanager
        List<String> reslist = new ArrayList<String>();
		
        try {
	        AssetManager am = currentSession.applicationContext.createPackageContext(packageName, 0).getAssets();
	        XmlResourceParser xml = am.openXmlResourceParser("AndroidManifest.xml");
	        
	        while (xml.next() != XmlPullParser.END_DOCUMENT) {
	        	if (xml.getEventType() == XmlPullParser.START_TAG && xml.getName().equals("data")) {
	    			if (xml.getAttributeCount() == 2 && xml.getAttributeValue(0).equals("android_secret_code"))
	    				reslist.add(xml.getAttributeValue(1));
	        	}
	        }
        } catch(Exception e) {
        	info.addAllSecretCode(new ArrayList<String>());
        	return;
        }
		// Send to client
		info.addAllSecretCode(reslist);
	}

}
