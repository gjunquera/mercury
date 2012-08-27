// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.ProviderResponse;
import com.mwr.mercury.Message.Response;
import com.mwr.mercury.Session;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.pm.PackageManager;
import android.content.pm.PathPermission;
import android.content.pm.ProviderInfo;
import android.database.Cursor;
import android.net.Uri;
import android.os.PatternMatcher;
import android.util.Base64;
import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Provider
{	
	
	public static void info(List<KVPair> argsArray, Session currentSession)
	{
		String filter = Common.getParamString(argsArray, "filter");
		String permissions = Common.getParamString(argsArray, "permissions");
		
		// Get all providers and iterate through them
		List<ProviderInfo> providers = currentSession.applicationContext
				.getPackageManager().queryContentProviders(null,
						PackageManager.GET_URI_PERMISSION_PATTERNS,
						PackageManager.GET_URI_PERMISSION_PATTERNS);

		ProviderResponse.Builder providerBuilder = ProviderResponse.newBuilder();
		// Iterate through content providers
		for (int i = 0; i < providers.size(); i++)
		{
			// Get all relevant info from content provider
			String providerAuthority = providers.get(i).authority;
			String providerPackage = providers.get(i).packageName;
			String providerReadPermission = providers.get(i).readPermission;
			PatternMatcher[] uriPermissionPatterns = providers.get(i).uriPermissionPatterns;
			String providerWritePermission = providers.get(i).writePermission;
			PathPermission[] providerPathPermissions = providers.get(i).pathPermissions;
			boolean providerMultiprocess = providers.get(i).multiprocess;
			boolean grantUriPermissions = providers.get(i).grantUriPermissions;

			boolean relevantFilter = false;
			boolean relevantPermissions = false;
			boolean noFilters = false;
			boolean bothFiltersRelevant = false;

			// Check if a filter was used
			if (filter.length() > 0)
				relevantFilter = providerAuthority.toUpperCase().contains(
						filter.toUpperCase())
						|| providerPackage.toUpperCase().contains(
								filter.toUpperCase());

			// Check if a permission filter was used
			try
			{
				if (permissions.length() > 0)
				{
					if (permissions.toUpperCase().equals("NULL"))
						relevantPermissions = (providerReadPermission == null)
								|| (providerWritePermission == null);
					else
						relevantPermissions = providerReadPermission.toUpperCase()
								.contains(permissions.toUpperCase())
								|| providerWritePermission.toUpperCase()
										.contains(permissions.toUpperCase());
				}
			}
			catch (Throwable t)
			{
			}

			// Check if no parameters were given
			if (filter.length() == 0 && permissions.length() == 0)
				noFilters = true;

			boolean bothFiltersPresent = false;
			if ((filter != "") && (permissions != ""))
				bothFiltersPresent = true;

			if (bothFiltersPresent && relevantFilter && relevantPermissions)
				bothFiltersRelevant = true;

			// Apply filter and only look @ exported providers
			if (((bothFiltersPresent && bothFiltersRelevant)
					|| (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters))
					&& providers.get(i).exported)
			{
				ProviderResponse.Info.Builder infoBuilder = ProviderResponse.Info.newBuilder();
				// URI Permission Patterns
				if (uriPermissionPatterns != null)
					for (int j = 0; j < uriPermissionPatterns.length; j++)
					{
						String path = uriPermissionPatterns[j].getPath();
						if (path != null)
							infoBuilder.addUriPermissionPatterns(path);
					}
				
				// Path permissions
				if (providerPathPermissions != null) 
					for (int j = 0; j < providerPathPermissions.length; j++)
					{
						if (providerPathPermissions[j].getReadPermission() != null)
						{
							ProviderResponse.Info.PatternPermission.Builder pathPermissionBuilder = 
											ProviderResponse.Info.PatternPermission.newBuilder();
							pathPermissionBuilder.setReadPermission(providerPathPermissions[j].getPath());
							pathPermissionBuilder.setReadNeeds(providerPathPermissions[j].getReadPermission());
							infoBuilder.addPathPermissions(pathPermissionBuilder);
						}

						if (providerPathPermissions[j].getWritePermission() != null)
						{
							ProviderResponse.Info.PatternPermission.Builder pathPermissionBuilder = 
								ProviderResponse.Info.PatternPermission.newBuilder();
							pathPermissionBuilder.setWritePermission(providerPathPermissions[j].getPath());
							pathPermissionBuilder.setWriteNeeds(providerPathPermissions[j].getWritePermission());
							infoBuilder.addPathPermissions(pathPermissionBuilder);
						}
					}
				
				if (providerReadPermission != null)
					infoBuilder.setReadPermission(providerReadPermission);

				if (providerWritePermission != null)
					infoBuilder.setWritePermission(providerWritePermission);
				
				infoBuilder.setAuthority(providerAuthority);
				infoBuilder.setPackageName(providerPackage);
				infoBuilder.setGrantUriPermissions(grantUriPermissions);
				infoBuilder.setMultiprocess(providerMultiprocess);
				providerBuilder.addInfo(infoBuilder);			
			}
		}
		
		Response response = Response.newBuilder().setData(providerBuilder.build().toByteString()).build();
		currentSession.send(Base64.encodeToString(response.toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
		
	}

	public static void columns(List<KVPair> argsArray,
			Session currentSession)
	{
		// Get list of columns
		ArrayList<String> columns = Common.getColumns(
				currentSession.applicationContext.getContentResolver(),
				Common.getParamString(argsArray, "uri"), null);

		Response.Builder respBuilder = Response.newBuilder();

		if (columns.size() == 0)
			respBuilder.setError(ByteString.copyFrom("Invalid content URI specified".getBytes()));
		else
		{
			KVPair.Builder pairBuilder = KVPair.newBuilder();
			// Iterate through columns
			for (int i = 0; i < columns.size(); i++)
			{
				pairBuilder.addValue(ByteString.copyFrom(columns.get(i).getBytes()));
			}
			pairBuilder.setKey("columns");
			respBuilder.addStructuredData(pairBuilder);
			respBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		}
		
		currentSession.send(Base64.encodeToString(respBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void query(List<KVPair> argsArray,
			Session currentSession)
	{

		Response.Builder respBuilder = Response.newBuilder();
		try
		{
			// Get content provider and cursor
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Get all the parameters
			List<String> projection = Common.getParamStringList(argsArray,
					"projection");
			String selection = Common.getParamString(argsArray, "selection");
			List<String> selectionArgs = Common.getParamStringList(argsArray,
					"selectionArgs");
			String sortOrder = Common.getParamString(argsArray, "sortOrder");
			String showColumns = Common
					.getParamString(argsArray, "showColumns");

			// Put projection in an array
			String[] projectionArray = null;
			if (projection.size() > 0)
			{
				projectionArray = new String[projection.size()];
				Iterator<String> it = projection.iterator();

				int i = 0;

				while (it.hasNext())
				{
					projectionArray[i] = it.next();
					i++;
				}
			}

			// Put selectionArgs in an array
			String[] selectionArgsArray = null;
			if (selectionArgs.size() > 0)
			{
				selectionArgsArray = new String[selectionArgs.size()];
				Iterator<String> it = selectionArgs.iterator();

				int i = 0;

				while (it.hasNext())
				{
					selectionArgsArray[i] = it.next();
					i++;
				}
			}

			// Issue query
			Cursor c = r.query(Uri.parse(new String(Common.getParam(argsArray,
					"Uri"))), projectionArray,
					(selection.length() > 0) ? selection : null,
					selectionArgsArray, (sortOrder.length() > 0) ? sortOrder
							: null);

			// Check if query failed
			if (c != null)
			{
				// Display the columns
				if (showColumns.length() == 0
						|| showColumns.toUpperCase().contains("TRUE"))
				{
					ArrayList<String> cols = Common.getColumns(r,
							Common.getParamString(argsArray, "Uri"),
							projectionArray);
					Iterator<String> it = cols.iterator();

					KVPair.Builder pairBuilder = KVPair.newBuilder();
					pairBuilder.setKey("columns");
					while (it.hasNext())
						pairBuilder.addValue(ByteString.copyFrom((it.next().getBytes())));
					respBuilder.addStructuredData(pairBuilder);
				}

				// Get all rows of data
				for (c.moveToFirst(); !c.isAfterLast(); c.moveToNext())
				{
					int numOfColumns = c.getColumnCount();
					String data = "";

					// Iterate through columns
					KVPair.Builder pairBuilder = KVPair.newBuilder();
					pairBuilder.setKey("line");
					for (int l = 0; l < numOfColumns; l++)
					{

						// Get string - if there is an error try retrieve as a
						// blob
						try
						{
							data = c.getString(l);
							if (data != null)
								pairBuilder.addValue(ByteString.copyFrom(data.getBytes()));
							else 
								pairBuilder.addValue(ByteString.copyFrom("null".getBytes()));
						}
						catch (Exception e)
						{
							// Base64 encode blobs and prepend with (blob)
							pairBuilder.addValue(ByteString.copyFrom(Base64.encodeToString(c.getBlob(l),
													Base64.DEFAULT).getBytes()));
						}
					}
					respBuilder.addStructuredData(pairBuilder);
				}
				respBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
				c.close();
			}
			else
			{
				respBuilder.setError(ByteString.copyFrom("QUERY FAILED".getBytes()));
			}

		}
		catch (Throwable t)
		{
			respBuilder.setError(ByteString.copyFrom(t.getMessage().getBytes()));
		}
		currentSession.send(Base64.encodeToString(respBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void read(List<KVPair> argsArray,
			Session currentSession)
	{

		Uri uri = Uri.parse(Common.getParamString(argsArray, "Uri"));
		ContentResolver r = currentSession.applicationContext
				.getContentResolver();
		InputStream is;
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
			is = r.openInputStream(uri);

			ByteArrayOutputStream baos = new ByteArrayOutputStream();
			int len = -1;
			do
			{
				byte[] buf = new byte[1024];
				len = is.read(buf);
				if (len > 0)
					baos.write(buf, 0, len);
	
			}
			while (len != -1);
	
			byte[] buf = baos.toByteArray();
			responseBuilder.setData(ByteString.copyFrom(buf));
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
			//String b64 = Base64.encodeToString(buf, 0);
		}
		catch (FileNotFoundException e)
		{
			responseBuilder.setError(ByteString.copyFrom("File not found".getBytes()));
			responseBuilder.setData(ByteString.copyFrom(("No files supported by provider at" 
														+ uri.toString()).getBytes()));
		}
		catch (IOException e)
		{
			responseBuilder.setError(ByteString.copyFrom(e.getMessage().getBytes()));
		}
		
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void insert(List<KVPair> argsArray,
			Session currentSession)
	{
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
			ContentValues contentvalues = new ContentValues();

			// Place values into contentvalue structure
			List<String> strings = Common.getParamStringList(argsArray,
					"string");
			if (strings != null)
				contentvalues.putAll(Common.listToContentValues(strings,
						"string"));

			List<String> booleans = Common.getParamStringList(argsArray,
					"boolean");
			if (booleans != null)
				contentvalues.putAll(Common.listToContentValues(booleans,
						"boolean"));

			List<String> integers = Common.getParamStringList(argsArray,
					"integer");
			if (integers != null)
				contentvalues.putAll(Common.listToContentValues(integers,
						"integer"));

			List<String> doubles = Common.getParamStringList(argsArray,
					"double");
			if (doubles != null)
				contentvalues.putAll(Common.listToContentValues(doubles,
						"double"));

			List<String> floats = Common.getParamStringList(argsArray, "float");
			if (floats != null)
				contentvalues.putAll(Common
						.listToContentValues(floats, "float"));

			List<String> longs = Common.getParamStringList(argsArray, "long");
			if (longs != null)
				contentvalues.putAll(Common.listToContentValues(longs, "long"));

			List<String> shorts = Common.getParamStringList(argsArray, "short");
			if (shorts != null)
				contentvalues.putAll(Common
						.listToContentValues(shorts, "short"));

			// Get content resolver
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Issue insert command
			Uri c = r.insert(
					Uri.parse(new String(Common.getParam(argsArray, "Uri"))),
					contentvalues);

			responseBuilder.setData(ByteString.copyFrom(c.toString().getBytes()));
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
			
		}
		catch (Throwable t)
		{
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_UNKNOWN.getBytes()));
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void update(List<KVPair> argsArray,
			Session currentSession)
	{
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
			ContentValues contentvalues = new ContentValues();

			// Place values into contentvalue structure
			List<String> strings = Common.getParamStringList(argsArray,
					"string");
			if (strings != null)
				contentvalues.putAll(Common.listToContentValues(strings,
						"string"));

			List<String> booleans = Common.getParamStringList(argsArray,
					"boolean");
			if (booleans != null)
				contentvalues.putAll(Common.listToContentValues(booleans,
						"boolean"));

			List<String> integers = Common.getParamStringList(argsArray,
					"integer");
			if (integers != null)
				contentvalues.putAll(Common.listToContentValues(integers,
						"integer"));

			List<String> doubles = Common.getParamStringList(argsArray,
					"double");
			if (doubles != null)
				contentvalues.putAll(Common.listToContentValues(doubles,
						"double"));

			List<String> floats = Common.getParamStringList(argsArray, "float");
			if (floats != null)
				contentvalues.putAll(Common
						.listToContentValues(floats, "float"));

			List<String> longs = Common.getParamStringList(argsArray, "long");
			if (longs != null)
				contentvalues.putAll(Common.listToContentValues(longs, "long"));

			List<String> shorts = Common.getParamStringList(argsArray, "short");
			if (shorts != null)
				contentvalues.putAll(Common
						.listToContentValues(shorts, "short"));

			List<String> selectionArgs = Common.getParamStringList(argsArray,
					"selectionArgs");
			String where = Common.getParamString(argsArray, "where");

			// Put selectionArgs in an array
			String[] selectionArgsArray = null;
			if (selectionArgs.size() > 0)
			{
				selectionArgsArray = new String[selectionArgs.size()];
				Iterator<String> it = selectionArgs.iterator();

				int i = 0;

				while (it.hasNext())
				{
					selectionArgsArray[i] = it.next();
					i++;
				}
			}

			// Get content resolver
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Issue update command
			Integer c = r.update(
					Uri.parse(Common.getParamString(argsArray, "Uri")),
					contentvalues, (where.length() > 0) ? where : null,
					selectionArgsArray);

			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
			KVPair.Builder pairBuilder = KVPair.newBuilder();
			pairBuilder.setKey("rows_updated");
			pairBuilder.addValue(ByteString.copyFrom((c.toString().getBytes())));
			responseBuilder.addStructuredData(pairBuilder);
		}
		catch (Throwable t)
		{
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_UNKNOWN.getBytes()));
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void delete(List<KVPair> argsArray,
			Session currentSession)
	{
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{

			List<String> selectionArgs = Common.getParamStringList(argsArray,
					"selectionArgs");
			String where = Common.getParamString(argsArray, "where");

			// Put selectionArgs in an array
			String[] selectionArgsArray = null;
			if (selectionArgs.size() > 0)
			{
				selectionArgsArray = new String[selectionArgs.size()];
				Iterator<String> it = selectionArgs.iterator();

				int i = 0;

				while (it.hasNext())
				{
					selectionArgsArray[i] = it.next();
					i++;
				}
			}

			// Get content resolver
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Issue delete command
			Integer rowsDeleted = r.delete(
					Uri.parse(Common.getParamString(argsArray, "Uri")),
					(where.length() > 0) ? where : null, selectionArgsArray);
			
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
			KVPair.Builder pairBuilder = KVPair.newBuilder();
			pairBuilder.setKey("rows_deleted");
			pairBuilder.addValue(ByteString.copyFrom((rowsDeleted.toString().getBytes())));
			responseBuilder.addStructuredData(pairBuilder);

		}
		catch (Throwable t)
		{
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_UNKNOWN.getBytes()));
		}
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

	public static void finduri(List<KVPair> argsArray, Session currentSession)
	{
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		ArrayList<String> lines = Common.strings(path);
		Iterator<String> it = lines.iterator();
		
		Response.Builder responseBuilder = Response.newBuilder();
		KVPair.Builder pairBuilder = KVPair.newBuilder();
		
		pairBuilder.setKey("uri");
		while (it.hasNext())
		{
			String next = it.next();
			
			if (next.toUpperCase().contains("CONTENT://") && !next.toUpperCase().equals("CONTENT://"))
				pairBuilder.addValue(ByteString.copyFrom(next.getBytes()));
		}
		
		responseBuilder.addStructuredData(pairBuilder);
		responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}

}