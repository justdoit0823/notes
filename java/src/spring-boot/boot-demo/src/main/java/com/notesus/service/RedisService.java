package com.notesus.service;

import org.springframework.stereotype.Service;

@Service
public class RedisService implements CacheService {

    @Override
    public boolean set(String key, String value) {
        System.out.println("set " + key + "'s value to " + value);
        return true;
    }

}
