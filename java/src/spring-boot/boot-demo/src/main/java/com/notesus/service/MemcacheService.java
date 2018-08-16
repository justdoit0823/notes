package com.notesus.service;

import org.springframework.stereotype.Service;

public class MemcacheService implements CacheService {

    @Override
    public boolean set(String key, String value) {
        System.out.println("set " + key + "'s value to " + value + " in memcache.");
        return true;
    }

}
