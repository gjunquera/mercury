// License: Refer to the README in the root directory

package com.mwr.mercury;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.Serializable;
import java.math.BigInteger;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Message.KVPair;

import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.res.AssetManager;
import android.content.res.XmlResourceParser;
import android.database.Cursor;
import android.net.Uri;
import android.util.Log;

//A class to wrap requests that come in
class RequestWrapper
{
	public String section;
	public String function;
	public List<KVPair> argsArray;
}

public class Common
{	
	public static final String ERROR_OK = "OK";
	public static final String ERROR_UNKNOWN = "ERROR";
	public static final short COMMAND_REQUEST = 0;
	public static final short COMMAND_REPLY = 1;
	public static final short REFLECTIVE_REQUEST = 2;
	public static final short REFLECTIVE_REPLY = 3;

	public enum Day {
	    SUNDAY, MONDAY, TUESDAY, WEDNESDAY,
	    THURSDAY, FRIDAY, SATURDAY 
	}
	
	public static final short version = 1;
	
	
	
	//Mercury persistent shell
	public static Shell mercuryShell = null;
	
	//Get all local IP addresses - needs INTERNET permission
	public static ArrayList<String> getLocalIpAddresses()
	{		
		
		ArrayList<String> ips = new ArrayList<String>();
		
	    try
	    {
	    	//Iterate over all network interfaces
	        for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();)
	        {
	        	//Get next network interface
	            NetworkInterface intf = en.nextElement();
	            
	            //Iterate over all IP addresses
	            for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();)
	            {
	            	//Get next IP address
	                InetAddress inetAddress = enumIpAddr.nextElement();
	                
	                //Add IP address if it is not a loopback address
	                if (!inetAddress.isLoopbackAddress())
	                	ips.add(inetAddress.getHostAddress().toString());
	                    
	            }
	        }
	        
	    }
	    catch (SocketException ex)
	    {
	        Log.e("getLocalIpAddress", ex.toString());
	    }
	    
	    return ips;
	}
	
	//Get md5Sum of file
	public static String md5SumFile(String path)
	{
		String md5 = "";
		
		try
		{
			MessageDigest digest = MessageDigest.getInstance("MD5");
			InputStream is = new FileInputStream(new File(path));				
			byte[] buffer = new byte[8192];
			int read = 0;
			try
			{
				while( (read = is.read(buffer)) > 0)
				{
					digest.update(buffer, 0, read);
				}	
				
				byte[] md5sum = digest.digest();
				BigInteger bigInt = new BigInteger(1, md5sum);
				md5 = bigInt.toString(16);
			}
			catch(IOException e)
			{
				throw new RuntimeException("Unable to process file for MD5", e);
			}
			finally
			{
				try
				{
					is.close();
				}
				catch(IOException e) {}
			}	
		}
		catch (Exception e) {}
		
		return md5;
	}
	
	
	//Get parameter from a List<KVPair> in byte[] format
	public static byte[] getParam(List<KVPair> pairsArray, String key)
	{
		
		if (key == null || pairsArray == null) 
			return null;
		
		for (KVPair pair : pairsArray) 
		{
			String pairKey = pair.getKey();
			if (pairKey != null) 
				if (pairKey.equalsIgnoreCase(key))
					return pair.getValueList().get(0).toByteArray();
		}
		return null;
	}
		
	//Get parameter from a List<Args>
	public static String getParamString(List<KVPair> pairsArray, String key) 
	{
		byte[] param = getParam(pairsArray, key);
		if (param == null) 
			return "";
		else return new String(param);
	}
	
	//Get parameter from a List<KVPair> in List<String> format
	public static List<String> getParamStringList(List<KVPair> pairsArray, String key)
	{
		List<String> returnValues = new ArrayList<String>();
		
		if (key == null || pairsArray == null) 
			return returnValues;
		
		for (int i = 0; i < pairsArray.size(); i++) 
		{
			KVPair pair = pairsArray.get(i);
			String pairKey = pair.getKey();
			if (pairKey != null) 
				if (pairKey.equalsIgnoreCase(key))
					for (int j = 0; j < pair.getValueList().size(); j++)
						returnValues.add(new String(pair.getValue(j).toByteArray()));
		}
		
		return returnValues;
	}

	
	//Convert a List to a contentvalues structure by splitting by =
	public static ContentValues listToContentValues(List<String> values, String type)
	{
		ContentValues contentvalues = new ContentValues();
	    
	    //Place values into contentvalue structure
	    for (int i = 0; i < values.size(); i++)
	    {
	    	String current = values.get(i);
	    	
	    	try
	    	{    	
		    	//Separate the value by = in order to get key:value
		    	Integer indexOfEquals = current.indexOf("=");
		    	String key = current.substring(0, indexOfEquals);
		    	String value = current.substring(indexOfEquals + 1);
		
		    	if (type.toUpperCase().equals("STRING"))
		    		contentvalues.put(key, value);
		    	
		    	if (type.toUpperCase().equals("BOOLEAN"))
		    		contentvalues.put(key, Boolean.valueOf(value));
	
		    	if (type.toUpperCase().equals("INTEGER"))
		    		contentvalues.put(key, new Integer(value));
		    	
		    	if (type.toUpperCase().equals("DOUBLE"))
		    		contentvalues.put(key, new Double(value));
		    	
		    	if (type.toUpperCase().equals("FLOAT"))
		    		contentvalues.put(key, new Float(value));
		    	
		    	if (type.toUpperCase().equals("LONG"))
		    		contentvalues.put(key, new Long(value));
		    	
		    	if (type.toUpperCase().equals("SHORT"))
		    		contentvalues.put(key, new Short(value));
	    	}
	    	catch (Exception e) 
	    	{
	    		Log.e("mercury", "Error with argument " + current);
	    	}
	    	
	    }
	    
	    return contentvalues;
	}
	
	//Get the columns of a content provider
	public static ArrayList<String> getColumns (ContentResolver resolver, String uri, String[] projectionArray)
	{
		//String returnValue = "";
		ArrayList<String> columns = new ArrayList<String>();
		
		try
		{				
	        //Issue query
	        Cursor c = resolver.query(Uri.parse(uri), projectionArray, null, null, null);
	                    		        	
	        //Get all column names and display
	        if (c != null)
	        {
	        	String [] colNames = c.getColumnNames();
	        	
	        	//Close the cursor
	        	c.close();
	        	
	        	//String columnNamesOutput = "";
	        	for (int k = 0; k < colNames.length; k++)
	        		columns.add(colNames[k]);
	        }
		}
		catch (Throwable t) {}
		
		return columns;
		

	}
	
	static {
		System.loadLibrary("mstring");
	}
	
	private static native String native_strings(String path);
	
	public static ArrayList<String> strings(String path) {
		ArrayList<String> lines = new ArrayList<String>();
		
		String nativeList = native_strings(path);
		
		if (nativeList != null) {		
			String[] stringList = nativeList.split("\n");
				
			if (stringList != null) {		
				for (String uri : stringList) {
					lines.add(uri);
				}
			}
		}
		
		return lines;
	}
	
	//Parse a generic intent and add to given intent
	public static Intent parseIntentGeneric(List<KVPair> argsArray, Intent intent)
	{		
		Intent localIntent = intent;
		
		//Iterate through arguments
		for (KVPair pair : argsArray)
		{
			
			String value = "";
			String valueArg = "";
			
			try
			{
				String key = pair.getKey();
				for (ByteString valueBytes : pair.getValueList()) {
					
					//Try split value into key=value pair
					String[] split = new String(valueBytes.toByteArray()).split("=");
					value = split[0];
					if (split.length > 1)
						valueArg = split[1];
					
					//Parse arguments into Intent
					if (key.equalsIgnoreCase("ACTION"))
						localIntent.setAction(value);
					
					else if (key.equalsIgnoreCase("DATA"))
						localIntent.setData(Uri.parse(value));
						
					else if (key.equalsIgnoreCase("MIMETYPE"))
						localIntent.setType(value);
	
					else if (key.equalsIgnoreCase("CATEGORY"))
						localIntent.addCategory(value);
						
					else if (key.equalsIgnoreCase("COMPONENT"))
						localIntent.setComponent(new ComponentName(value, valueArg));
						
					else if (key.equalsIgnoreCase("FLAGS"))
						localIntent.setFlags(Integer.parseInt(new String(value)));
						
					else if (key.equalsIgnoreCase("EXTRABOOLEAN"))
						localIntent.putExtra(value, Boolean.parseBoolean(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRABYTE"))
						localIntent.putExtra(value, Byte.parseByte(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRADOUBLE"))
						localIntent.putExtra(value, Double.parseDouble(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRAFLOAT"))
						localIntent.putExtra(value, Float.parseFloat(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRAINTEGER"))
						localIntent.putExtra(value, Integer.parseInt(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRALONG"))
						localIntent.putExtra(value, Long.parseLong(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRASERIALIZABLE"))
						localIntent.putExtra(value, Serializable.class.cast(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRASHORT"))
						localIntent.putExtra(value, Short.parseShort(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRASTRING"))
						localIntent.putExtra(value, valueArg);
						
				}
			}
			catch (Exception e)
			{
				Log.e("mercury", "Error with argument " + pair.getKey());
			}
			
		}
		
		return localIntent;
	}

	//Extract the src file to dest - return success
	public static boolean unzipFile(String filename, String src, String dest)
	{
		final int BUFFER_SIZE = 4096;
		boolean success = false;
		String fname = filename.toUpperCase();
		  
		BufferedOutputStream bufferedOutputStream = null;
		FileInputStream fileInputStream;
		try
		{
			fileInputStream = new FileInputStream(src);
			ZipInputStream zipInputStream = new ZipInputStream(new BufferedInputStream(fileInputStream));
			ZipEntry zipEntry;
		      
			while ((zipEntry = zipInputStream.getNextEntry()) != null)
			{
				String zipEntryName = zipEntry.getName();
				if (zipEntryName.toUpperCase().equals(fname))
				{
					File file = new File(dest + zipEntryName);
					byte buffer[] = new byte[BUFFER_SIZE];
					FileOutputStream fileOutputStream = new FileOutputStream(file);
					bufferedOutputStream = new BufferedOutputStream(fileOutputStream, BUFFER_SIZE);
					int count;

					while ((count = zipInputStream.read(buffer, 0, BUFFER_SIZE)) != -1)
					{
						bufferedOutputStream.write(buffer, 0, count);
					}

					bufferedOutputStream.flush();
					bufferedOutputStream.close();
					
					success = true;
				}

			}
			zipInputStream.close();
		}
		catch (Exception e)
		{
			Log.e("mercury", e.getMessage());
		}

			   
		return success;

	}
	
	public static KVPair createKVPair(String key, String value) {
		return createKVPair(key, ByteString.copyFrom(value.getBytes()));
	}
	
	public static KVPair createKVPair(String key, List<String> values) {
		KVPair.Builder pairBuilder = KVPair.newBuilder();
		pairBuilder.setKey(key);
		for (String value : values)
			pairBuilder.addValue(ByteString.copyFrom(value.getBytes()));
		return pairBuilder.build();
	}
	
	public static KVPair createKVPair(String key, ByteString value) {
		KVPair.Builder pairBuilder = KVPair.newBuilder();
		pairBuilder.setKey(key);
		pairBuilder.addValue(value);
		return pairBuilder.build();
	}
	
	// Added in order to get the actions of each broadcast receiver
	// Change added by Luander Ribeiro <luander.r@samsung.com>
	// in Aug 27 - 2012
	/**
	 * Get a list of actions of a given receiver
	 * @param currentSession the session for current request
	 * @param receivers An ActivityInfo with information about the receiver
	 * @param parentTag Name of the tag where intent filter actions will be searched inside
	 * @return A list of strings containing the actions of a receiver or an empty list, if there is no action
	 */
	public static List<String> findIntentFilterActions(Session currentSession, ActivityInfo receiver, String parentTag) {
		return findIntentFilterActions(currentSession, receiver.packageName, receiver.name, parentTag);
	}
	
	// Added in order to get the actions of each broadcast receiver
	// Change added by Luander Ribeiro <luander.r@samsung.com>
	// in Aug 27 - 2012
	/**
	 * Get a list of actions of a given receiver
	 * @param currentSession the session for current request
	 * @param receivers An ActivityInfo with information
	 * @param parentTag Name of the tag where intent filter actions will be searched inside
	 * @return A list of strings containing the actions of a receiver or an empty list, if there is no action
	 */
	public static List<String> findIntentFilterActions(Session currentSession, String packageName, String className, String parentTag)
	{
		List<String> actions = new ArrayList<String>();
		try
		{
			AssetManager am = currentSession.applicationContext.createPackageContext(packageName, 0).getAssets();
			XmlResourceParser xml = am.openXmlResourceParser("AndroidManifest.xml");

			//XML parsing
			while (xml.next() != XmlPullParser.END_DOCUMENT) {
				switch (xml.getEventType()) {
				case XmlPullParser.START_TAG:
					// Find receiver tag to start looking for intent filters
					if (parentTag.equals(xml.getName()))
					{
						String receiverName = searchXmlAttr(xml, "android:name");
						if (receiverName.length() == 0)
						{
							receiverName = searchXmlAttr(xml, "name");
						}
						// If the tag name matches with receiver, search for its intent filters
						if (receiverName.length() > 0 &&
								className.endsWith(receiverName))
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
