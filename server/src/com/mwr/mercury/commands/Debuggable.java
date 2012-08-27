// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import java.util.ArrayList;
import java.util.List;

import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.util.Base64;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.DebugResponse;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Session;
import com.mwr.mercury.Message.Response;

public class Debuggable
{
	public static void info(List<KVPair> argsArray, Session currentSession){
		//Assign filter if one came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		
		Response.Builder responseBuilder = Response.newBuilder();
		DebugResponse.Builder debugBuilder = DebugResponse.newBuilder();
		responseBuilder.setError(ByteString.copyFrom("No debuggable applications found".getBytes()));
		
		//Get all packages from packagemanager
		List <PackageInfo> packages = currentSession.applicationContext.getPackageManager().getInstalledPackages(PackageManager.GET_PERMISSIONS);
		
		//Iterate through packages
		for (PackageInfo package_:packages)
		{
			ApplicationInfo app = package_.applicationInfo;
			
			//Focus on debuggable apps only and apply filter
			if (((app.flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0) && (app.packageName.toUpperCase().contains(filter.toUpperCase()) || app.processName.toUpperCase().contains(filter.toUpperCase()) || filter == ""))
            {
				DebugResponse.Info.Builder infoBuilder = DebugResponse.Info.newBuilder();
				infoBuilder.setPackageName(app.packageName);
				infoBuilder.setUid(app.uid);
            	//Find all permissions that this app has
            	String[] permissions = package_.requestedPermissions;
            	
        		List<String> permissionList = new ArrayList<String>();
            	if (permissions != null)
            	{
            		for (String permission:permissions)
            			permissionList.add(permission);
            	}
            	infoBuilder.addAllPermission(permissionList);
            	debugBuilder.addInfo(infoBuilder);
        		responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
            }
		}
		responseBuilder.setData(debugBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

}
