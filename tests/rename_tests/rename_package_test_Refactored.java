package com.jsoniter;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.type.TypeReference;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.annotations.SerializedName;
import com.jsoniter.extra.GsonCompatibilityMode;
import com.jsoniter.spi.DecodingMode;
import com.jsoniter.spi.JsoniterSpi;
import org.openjdk.jmh.Main;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.BenchmarkParams;
import org.openjdk.jmh.infra.Blackhole;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Date;
import java.util.List;


class SuggestedRoomsByFollowingsListViewAdapter extends BaseAdapter {
    Context mContext;
    LayoutInflater inflater;
    private List<InputRoomSuggestSearchViewModel> SearchedRoomsList = null;

    public SuggestedRoomsByFollowingsListViewAdapter(Context context, List<InputRoomSuggestSearchViewModel> SearchedPersonsList) {
        mContext = context;
        this.SearchedRoomsList = SearchedPersonsList;
        inflater = LayoutInflater.from(mContext);
    }

    private CreateRoomViewModel RoomModel(String name) {
        CreateRoomViewModel RoomModel = new CreateRoomViewModel(name, description, CreateInterests(), startDate, endDate);
        return RoomModel;
    }

    public String testCall(Date D1){
        RoomModel("a");
        return "x";
    }
}


class SuggestedRoomsByFollowingsListViewAdapter2 {

    Context mContext;
    LayoutInflater inflater;
    private List<InputRoomSuggestSearchViewModel> SearchedRoomsList = null;

    public SuggestedRoomsByFollowingsListViewAdapter2(Context context, List<InputRoomSuggestSearchViewModel> SearchedPersonsList) {
        mContext = context;
        this.SearchedRoomsList = SearchedPersonsList;
        inflater = LayoutInflater.from(mContext);

    }


    private CreateRoomViewModel RoomModel(String name, String description, Date startDate, Date endDate) {
        CreateRoomViewModel RoomModel = new CreateRoomViewModel(name, description, CreateInterests(), startDate, endDate);
        return RoomModel;
    }
}