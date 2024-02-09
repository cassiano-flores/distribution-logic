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
            // URL da API
            JSONArray assetsRequest = getAssetsBR();

            for (int i = 0; i < usAssets.length; i++) {
              assetsRequest.put(getAssetUS(usAssets[i]));
            }

            // Calculando o valor total dos ativos atuais
            for (int i = 0; i < assetsBR.length(); i++) {
                JSONObject stockObject = assetsBR.getJSONObject(i);
                String name = stockObject.getString("stock");
                double price = stockObject.getDouble("close");

                if (containsAsset(name)) {
                    myAssets[index] = new Asset(name, price, MyAssets.valueOf(name).getQuantity(), MyAssets.valueOf(name).getTargetPercent());
                    sum += myAssets[index].getQuantity() * myAssets[index].getPrice();
                    index++;
                }
            }

            // Reserva de emerg�ncia
            myAssets[index] = new Asset("RE", 1, MyAssets.valueOf("RE").getQuantity(), MyAssets.valueOf("RE").getTargetPercent());
            sum += myAssets[index].getQuantity();

            while (contribution > 0) {
                Asset assetToAdd = getAssetToAdd(myAssets, sum);

                // Calcular o valor a ser investido neste ativo
                double valueToInvest = assetToAdd.getMinimumTick();

                if (contribution < valueToInvest) {
                    break;
                }

                assetToAdd.setQuantity(assetToAdd.getQuantity() + 1);
                contribution -= valueToInvest;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        printReport(myAssets);
    }

    private static JSONArray getAssetsBR() throws IOException {
        URL url = new URL("https://brapi.dev/api/quote/list?sortBy=name&sortOrder=asc&token=2RpfSrYsBy4i23T6TLdZa2");

        // Abrindo conexão HTTP
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
        return jsonResponse.getJSONArray("stocks");
    }

    private static JSONObject getAssetUS(String ticker) throws IOException {
        URL url = new URL("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=GQYE5EC48N9SSD0T");

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

        // Obtendo o objeto "Time Series (Daily)"
        JSONObject timeSeriesDaily = jsonResponse.getJSONObject("Time Series (Daily)");

        // Obtendo a primeira chave (data) dentro de "Time Series (Daily)"
        String firstDate = timeSeriesDaily.keys().next();

        // Obtendo o primeiro objeto dentro de "Time Series (Daily)"
        JSONObject firstObject = timeSeriesDaily.getJSONObject(firstDate);

        // Removendo a chave "data"
        timeSeriesDaily.remove(firstDate);

        // Criando uma propriedade "stock" no objeto e definindo seu valor como o ticker
        firstObject.put("stock", ticker);

        // Retornando o objeto modificado
        return firstObject;
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
/*         if (args.length == 0) {
            System.out.println("Not a valid contribution.");
            return;
        } */

        // getDistribution(Integer.parseInt(args[0]));
        getDistribution(5000);
    }
}
