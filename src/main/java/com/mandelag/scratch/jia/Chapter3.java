package com.mandelag.scratch.jia;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.List;
import java.util.Map;


public class Chapter3 {

    public static void main(String[] args) throws IOException {
        loadData();
    }

    private static void loadData() throws IOException {
        System.out.println(Paths.get("").toAbsolutePath().toFile().isDirectory());
        Path toData = Paths.get("src", "main", "resources", "TPS_Jakarta_2017.json");
        // kalau pakai backslash ngga bisa di *nix. Kalau pakai slash ngga bisa di Windows..?
        System.out.println(toData.toFile().exists());
        ObjectMapper om = new ObjectMapper();
        List<Map<String, String>> data = om.readValue(toData.toFile(), List.class);
        Base64.Encoder encoder = Base64.getEncoder();
        data.parallelStream()
                .map(m -> m.get("kelurahan"))
                .map(kelurahan -> {
                    byte[] encoded = encoder.encode(String.format("getTps~20181120Sm4RTC1tY~%s", kelurahan).getBytes());
                    return new String(encoded);
                })
                .forEach((command) -> {
                    System.out.println(String.format("http://crop.jakarta.go.id/ajax/apps_command.php?%s", command));
                });
    }

}
