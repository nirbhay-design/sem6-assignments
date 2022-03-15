#include <bits/stdc++.h>
#include <iostream>
#define N 256

using namespace std;
string convert(int n,int c){
    string a="";
    for(int i=0;i<=c;i++){
        if((1LL<<i)&n){
            a+='1';

        }
        else{
            a+='0';
        }
    }
    reverse(a.begin(),a.end());
    return a;
}
vector<int> KSA(vector<int> key){
    int n=key.size();
    vector<int> S(N);
    for(int i=0;i<N;i++){
        S[i]=i;
    }
    int j=0;
    for(int i=0;i<N;i++){
        j=(j+S[i]+(key[i%n]));
        j%=N;
        swap(S[i],S[j]);
    }
    return S;
}

vector<int> PRGA(vector<int> S,vector<int> pt){
    int n=pt.size();
    int i=0,j=0;
    vector<int> v;
    while(n--){
        i=(i+1)%N;
        j=(j+S[i])%N;
        swap(S[i],S[j]);
        int K=S[(S[i]+S[j])%N];
        //cout<<K<<endl;
        v.push_back(K);

    }
    return v;
}
vector<int> XOR(vector<int> pt,vector<int> v){
    int n=pt.size();
    vector<int> c(n,0);
    for(int i=0;i<n;i++){
        c[i]=((pt[i])^v[i]);

    }
    return c;
}

string encrypt(vector<int> pt,vector<int> key){
    vector<int> S=KSA(key);
    vector<int> k=PRGA(S,pt);
    vector<int> v=XOR(pt,k);
    for(int x:k){
        cout<<x<<" ";
    }
    cout<<endl;
    int cnt=0;
    int m=N;
    while(m>1){
        m/=2;
        cnt++;
    }
    string ans="";
    for(int x:v){
        ans+=convert(x,cnt-1);
    }
    return ans;
    

    //return ans;

}


int main(){
    //freopen("input1.txt", "r", stdin);
    //freopen("output.txt", "w", stdout);
    cout<<fixed<<setprecision(20);

    vector<int> pt;
    // cout<<"Enter size of plainText"<<endl;
    int n;
    cin>>n;
    for(int i=0;i<n;i++){
        int x;
        cin>>x;
        pt.push_back(x);
    }

    map<long long,long long> mp;
    int maxa=100000;
    while(maxa--){
    for(int i=1;i<=256;i++){
        int m=i;
        srand(time(NULL));
        vector<int> key;
        for(int j=0;j<m;j++){
            int x=rand()%100000;
            key.push_back(x);


        }
        vector<int> v1=KSA(key);
        vector<int> v2=PRGA(v1,pt);
        mp[v2[1]]++;
        //cout<<v2[1]<<endl;


    }
    }
    double p2=0;
    for(auto x:mp){
        // c+=(x.second);
        cout<<x.first<<":"<<x.second<<endl;
        p2+=x.second;


    }
    double p1=mp[0];
    cout<<p1/p2<<endl;
    
    //double ans=mp[0]/c*1.0;
    //cout<<ans<<endl;

    //cout<<"Ciphertext: ";
    //cout<<encrypt(pt,key);
    return 0;

    
}