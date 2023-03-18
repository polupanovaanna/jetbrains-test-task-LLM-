package com.jb_test_task.check_copypaste.controller;


import com.jb_test_task.check_copypaste.Data;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.*;
import java.util.List;
import java.util.stream.Collectors;


@Controller
public class CheckController {

    @GetMapping("/check")
    public String checkForm(Model model) {
        model.addAttribute("data", new Data());
        return "data";
    }

    @PostMapping("/check")
    public String dataSubmit(@ModelAttribute Data data, Model model) {

        try(FileWriter writer = new FileWriter("tttt.txt", false))
        {
            String text = data.getContent();
            writer.write(text);
            writer.flush();
            ProcessBuilder processBuilder = new ProcessBuilder("python3", resolvePythonScriptPath("check_file.py"));
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();
            List<String> results = readProcessOutput(process.getInputStream());
            if (!results.isEmpty()) {
                Data dt = new Data();
                dt.setContent(results.toString());
                model.addAttribute("data", dt);
            } else {
                model.addAttribute("data", data);
            }
        } catch(IOException ex){
            Data dt = new Data();
            dt.setContent(ex.toString());
            model.addAttribute("data", dt);
        }

        return "result";
    }

    private String resolvePythonScriptPath(String path){
        File file = new File(path);
        return file.getAbsolutePath();
    }
    private List<String> readProcessOutput(InputStream inputStream) throws IOException {
        try (BufferedReader output = new BufferedReader(new InputStreamReader(inputStream))) {
            return output.lines()
                    .collect(Collectors.toList());
        }
    }
}
