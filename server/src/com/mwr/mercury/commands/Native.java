package com.mwr.mercury.commands;

import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.util.Base64;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.NativeResponse;
import com.mwr.mercury.Session;
import com.mwr.mercury.Message.Response;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public class Native
{
	public static void info(List<KVPair> argsArray, Session currentSession) {
		
		//Assign filter if one came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		
		//Get all packages from packagemanager
		List <PackageInfo> packages = currentSession.applicationContext.getPackageManager().getInstalledPackages(PackageManager.GET_PERMISSIONS);
		
		//Iterate through packages
		ZipFile zipFile;
		boolean native_found;
		
		Response.Builder responseBuilder = Response.newBuilder();
		NativeResponse.Builder nativeBuilder = NativeResponse.newBuilder();
		responseBuilder.setError(ByteString.copyFrom("No applications found containing native code".getBytes()));
		for (PackageInfo package_:packages)
		{
			ApplicationInfo app = package_.applicationInfo;
			
			//Apply filter
			if ((app.packageName.toUpperCase().contains(filter.toUpperCase()) || app.processName.toUpperCase().contains(filter.toUpperCase()) || filter == ""))
            {
				native_found = false;
        		List<String> nativeList = new ArrayList<String>();
        		
				try {
		        	zipFile = new ZipFile(app.publicSourceDir);
			    	   
		        	Enumeration<? extends ZipEntry> entries = zipFile.entries();
			    
		        	ZipEntry entry;
		        	while(entries.hasMoreElements()) {
		        		entry = entries.nextElement();
		        		String name = entry.getName();
			    		
		        		if(name.endsWith(".so") | name.endsWith(".SO")| name.endsWith(".So") | name.endsWith(".sO")) {
		        			nativeList.add(name);
		        			native_found = true;
		        		}
		        	}
			    	   			    	   
				} catch (IOException e) {
					responseBuilder.setError(ByteString.copyFrom(("Error processing package '" + app.packageName + 
											"': " + e.getMessage()).getBytes()));
				}
				
				if(native_found) {
					NativeResponse.Info.Builder infoBuilder = NativeResponse.Info.newBuilder();
					infoBuilder.setPackageName(app.packageName);
					infoBuilder.addAllNativeLib(nativeList);
					nativeBuilder.addInfo(infoBuilder);
					responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));				
				}
            }
		}
		
		responseBuilder.setData(nativeBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}
}
