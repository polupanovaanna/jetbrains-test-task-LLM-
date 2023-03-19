package ru.fmcs.hse.amisquestions;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.fragment.app.Fragment;
import androidx.navigation.Navigation;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import com.mikepenz.materialdrawer.Drawer;
import com.mikepenz.materialdrawer.DrawerBuilder;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

import ru.fmcs.hse.amisquestions.databinding.FragmentCreateNewPostBinding;
import ru.fmcs.hse.database.Controller;

public class CreateNewPost extends Fragment {

    private FragmentCreateNewPostBinding mBinding;
    Toolbar mToolbar;
    private Drawer mDrawer;
    MarkdownTextView MTV;
    Button postButton;

    TagsList tags;

    private FirebaseAuth mFirebaseAuth;

    public void setText(String text) {
        MTV.setText(text);
    }

    public String getUserId() {
        FirebaseUser user = mFirebaseAuth.getCurrentUser();
        if (user != null) {
            return user.getUid();
        }
        return "err";
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        mFirebaseAuth = FirebaseAuth.getInstance();
        mBinding = FragmentCreateNewPostBinding.inflate(getLayoutInflater());
        return mBinding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        mToolbar = view.findViewById(R.id.toolbar2);
        MTV = view.findViewById(R.id.markdown_text);
        tags = view.findViewById(R.id.tags_list_add);
        postButton = view.findViewById(R.id.post_button);
        Controller.getAllTags((list) -> {
            tags.setTags(list);
        });

        postButton.setOnClickListener(view1 -> {
            String post = MTV.getText();
            String id = Controller.addPost(post, getUserId());
            StringBuilder stringBuilder = new StringBuilder();
            for (String tag : tags.getMarkedTags()) {
                Controller.addTag(id, tag);
                stringBuilder.append("'" + tag + "'" + " in topics || ");
                stringBuilder.setLength(stringBuilder.length() - 4);
                //это посылка уведомления всем подписанным на тег при создании поста
            }
            if (!(stringBuilder.length() == 0)) {
                sendNotification(stringBuilder.toString());
            }
            Navigation.findNavController(view1).navigate(R.id.mainPages);
        });

        mToolbar.setTitle("Добавление поста");

        mToolbar.setNavigationOnClickListener(v -> getActivity().onBackPressed());
    }

    private ActionBar getSupportActionBar() {
        return ((AppCompatActivity) getActivity()).getSupportActionBar();
    }

    private void createDrawer() {

        mDrawer = new DrawerBuilder()
                .withActivity(((AppCompatActivity) getActivity()))
                .withToolbar(mToolbar)
                .build();
    }

    private void sendNotification(String topic) {
        //String DeviceIdKey = "/topics/" + topic;
        String authKey = "";
        String FMCurl = "https://fcm.googleapis.com/fcm/send";

        try {
            URL url = new URL(FMCurl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();

            conn.setUseCaches(false);
            conn.setDoInput(true);
            conn.setDoOutput(true);

            conn.setRequestMethod("POST");
            conn.setRequestProperty("Authorization", "key=" + authKey);
            conn.setRequestProperty("Content-Type", "application/json");
            JSONObject data = new JSONObject();
            data.put("condition", topic);

            JSONObject info = new JSONObject();
            info.put("title", "FCM Notificatoin Title"); // Notification title
            info.put("body", "Hello First Test notification"); // Notification body
            data.put("notification", info);

            System.out.println(data.toString());
            OutputStreamWriter wr = new OutputStreamWriter(conn.getOutputStream());
            wr.write(data.toString());
            wr.flush();
            wr.close();

            int responseCode = conn.getResponseCode();
            System.out.println("Response Code : " + responseCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            System.out.println("Resonse: " + response);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}