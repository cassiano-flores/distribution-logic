import org.json.JSONArray;
import org.json.JSONObject;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {

    public static void getDistribution(double contribution) {
        Asset[] myAssets = new Asset[MyAssets.values().length];
        int index = 0;
        double sum = 0;

        // US Assets
        String[] usAssets = new String[] {"DLR","O","STAG","SPG","AMT","ARR","VOO"};

        try {
            // ATIVOS BR (65%)
            JSONArray assetsRequest = getAssetsBR();

            // ATIVOS CRYPTO (5%)
            JSONArray otherAssets = getAssetsCrypto();

            // ATIVOS US (20%)
            for (int i = 0; i < usAssets.length(); i++) {
                otherAssets.put(getAssetUS(usAssets[i]));
            }

            // Cria Asset para US e Crypto que ter�o MinimumTick 0.0001
            for ( ; index < otherAssets.length(); index++) {
                JSONObject stockObject = otherAssets.getJSONObject(index);
                String name = stockObject.getString("stock");
                double price = stockObject.getDouble("close");

                myAssets[index] = new Asset(name, price, MyAssets.valueOf(name).getQuantity(), MyAssets.valueOf(name).getTargetPercent(), 0.0001);
                sum += myAssets[index].getQuantity() * myAssets[index].getPrice();
            }

            // Cria Asset para BR
            for ( ; index < (otherAssets.length() + assetsRequest.length()); index++) {
                JSONObject stockObject = assetsRequest.getJSONObject(index);
                String name = stockObject.getString("stock");
                double price = stockObject.getDouble("close");

                myAssets[index] = new Asset(name, price, MyAssets.valueOf(name).getQuantity(), MyAssets.valueOf(name).getTargetPercent(), 1);
                sum += myAssets[index].getQuantity() * myAssets[index].getPrice();
            }

            // RESERVA DE EMERG�NCIA (10%)
            myAssets[index] = new Asset("RE", 1, MyAssets.valueOf("RE").getQuantity(), MyAssets.valueOf("RE").getTargetPercent(), 1);
            sum += myAssets[index].getQuantity();

            while (contribution > 0) {
                Asset assetToAdd = getAssetToAdd(myAssets, sum);

                // Calcular o valor a ser investido neste ativo
                double valueToInvest = assetToAdd.getMinimumTick() * assetToAdd.getPrice();

                if (contribution < valueToInvest) {
                    break;
                }

                assetToAdd.setQuantity(assetToAdd.getQuantity() + assetToAdd.getMinimumTick());
                contribution -= valueToInvest;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        printReport(myAssets);
    }

    private static JSONArray getAssetsBR() throws IOException {
        URL url = new URL("https://brapi.dev/api/quote/list?sortBy=name&sortOrder=asc&token=2RpfSrYsBy4i23T6TLdZa2");

        // Abrindo conex�o HTTP
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");

        // Lendo a resposta
        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        // Convertendo a resposta para JSON
        JSONObject jsonResponse = new JSONObject(response.toString());

        // Obtendo o array de stocks
        JSONArray allStocks = jsonResponse.getJSONArray("stocks");

        // Criando um novo JSONArray para armazenar os objetos filtrados
        JSONArray filteredStocks = new JSONArray();

        // Filtrando os objetos e adicionando-os ao novo JSONArray
        for (int i = 0; i < allStocks.length(); i++) {
            JSONObject stockObject = allStocks.getJSONObject(i);
            String stockName = stockObject.getString("stock");
            if (containsAsset(stockName)) {
                filteredStocks.put(stockObject);
            }
        }

        return filteredStocks;
    }

    private static JSONObject getAssetUS(String ticker) throws IOException {
        URL url = new URL("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=GQYE5EC48N9SSD0T");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");

        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        JSONObject jsonResponse = new JSONObject(response.toString());
        JSONObject timeSeriesDaily = jsonResponse.getJSONObject("Time Series (Daily)");
        String firstDate = timeSeriesDaily.keys().next();
        JSONObject firstObject = timeSeriesDaily.getJSONObject(firstDate);
        timeSeriesDaily.remove(firstDate);
        firstObject.put("stock", ticker);

        double closePrice = firstObject.getDouble("close");
        double dollarPrice = getDollarPrice();
        firstObject.put("close", closePrice * dollarPrice);

        return firstObject;
    }

    private static JSONArray getAssetsCrypto() throws IOException {
        URL url = new URL("https://economia.awesomeapi.com.br/last/BTC-BRL,ETH-BRL");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");

        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        // Convertendo a resposta para JSON
        JSONObject jsonResponse = new JSONObject(response.toString());

        // Criando um novo JSONArray para armazenar os objetos filtrados
        JSONArray filteredAssets = new JSONArray();

        // Iterando sobre as chaves do objeto JSON
        Iterator<String> keys = jsonResponse.keys();
        while (keys.hasNext()) {
            JSONObject asset = jsonResponse.getJSONObject(keys.next());

            // Removendo a propriedade "code" e substituindo por "stock"
            String stockName = asset.getString("code")
            asset.remove("code");
            asset.put("stock", stockName);

            // Renomeando a propriedade "bid" para "close"
            double closePrice = asset.getDouble("bid");
            asset.remove("bid");
            asset.put("close", closePrice);

            // Adicionando o objeto modificado ao novo JSONArray
            filteredAssets.put(asset);
        }

        return filteredAssets;
    }

    private static double getDollarPrice() throws IOException {
        URL url = new URL("https://economia.awesomeapi.com.br/last/USD-BRL");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");

        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        JSONObject jsonResponse = new JSONObject(response.toString());
        JSONObject usdbrl = jsonResponse.getJSONObject("USDBRL");
        return usdbrl.getDouble("high");
    }

    private static Asset getAssetToAdd(Asset[] myAssets, double sum) {
        double maxDifference = Double.NEGATIVE_INFINITY;
        Asset assetToAdd = null;

        // Calculando as diferenças para cada ativo
        for (Asset myAsset : myAssets) {
            double targetPercent = myAsset.getTargetPercent();
            double currentPercent = (((myAsset.getQuantity() * myAsset.getPrice()) * 100) / sum) / 100;
            double difference = targetPercent - currentPercent;

            if (difference > maxDifference) {
                // Atualizando o maior diferencial
                maxDifference = difference;
                assetToAdd = myAsset;
            }
        }
        return assetToAdd;
    }

    private static boolean containsAsset(String assetNameAPI) {
        for (MyAssets asset : MyAssets.values()) {
            if (asset.name().equals(assetNameAPI))
                return true;
        }
        return false;
    }

    private static void printReport(Asset[] myAssets) {
        try {
            String filePath = "D:\\Repos\\distribution-logic\\report.txt";

            // Criação do FileWriter para escrever no arquivo "report.txt"
            FileWriter fw = new FileWriter(filePath);
            BufferedWriter bw = new BufferedWriter(fw);

            bw.write("--------- RELATÓRIO DE DISTRIBUIÇÃO DO APORTE ---------");
            bw.newLine();
            bw.write("*******************************************************");
            bw.newLine();

            // Exibir os aportes sugeridos e a quantidade adicional no arquivo
            for (Asset asset : myAssets) {
                String assetName = asset.getName();
                String quantity = String.format("%.5f", asset.getQuantity());
                double additionalQuantity = asset.getQuantity() - MyAssets.valueOf(assetName).getQuantity();
                String additionalQuantityString = String.format("%.5f", additionalQuantity);

                bw.write(String.format("Ativo: %-7s; Quantidade sugerida: %-10s; Quantidade adicional: %-10s", assetName, quantity, additionalQuantityString));
                bw.newLine();
            }

            bw.write("*******************************************************");

            // Fechamento do BufferedWriter
            bw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Not a valid contribution.");
            return;
        }

        getDistribution(Integer.parseInt(args[0]));
    }
}
