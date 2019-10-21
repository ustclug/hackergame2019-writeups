#include <vector>
#include <memory>
#include <limits>
#include <cmath>
#include <cstdlib>
#include <cassert>
#include <cstdint>
#include <cstring>

using namespace std;

float cUCT = 0.4;
float bUCT = -1;
int depth = 300;
int playouts = 10000;

#include "idn.h"
#include "idm.h"

template<size_t ArraySize>
class Graph {
public:
    Graph(){
        for(size_t i = 0; i < ArraySize; i++){
            for(size_t j = 0; j < ArraySize; j++){
                if(idm[i*ntotal+j]!=0){
                    csr[i].push_back(j);
                    weight[i].push_back(idm[i*ntotal+j]);
                }
            }
        }
    }
    void Decrease(int cur, int next){
        for(size_t i = 0; i < csr[cur].size(); i++){
            if(csr[cur][i] == next){
                weight[cur][i]--;
                if (weight[cur][i] == 0){
                    csr[cur].erase(csr[cur].begin()+i);
                    weight[cur].erase(weight[cur].begin()+i);
                }
                return;
            }
        }
        assert(0);
    }
    vector<uint16_t> csr[ArraySize];
    vector<int8_t> weight[ArraySize];
};

class MCTSNode {
public:
    MCTSNode(Graph<nkernel>* g_, int cur_, int player_, MCTSNode* parent_, uint32_t seed_):
        cur(cur_), player(player_), g(g_), parent(parent_), q(0), n(0), seed(seed_){}
    MCTSNode* SelectExpand(){
        if(isKernelTerminal()){
            return this;
        }
        if(GetKernelAvail().size() > child.size()){
            Expand(GetKernelAvail()[child.size()]);
            return child.back().get();
        }
        return UCT(cUCT)->SelectExpand();
    }
    int Rollout(){
        struct {
            uint16_t start;
            uint16_t end;
        } ptr[nkernel];
        int length = 0;
        for(int i = 0; i < nkernel; i++){
            ptr[i].start = length;
            length += g->csr[i].size();
            ptr[i].end = length;
        }
        uint16_t* csr = (uint16_t*)alloca(sizeof(uint16_t)*length);
        uint8_t* weight = (uint8_t*)alloca(sizeof(uint8_t)*length);
        for(int i = 0; i < nkernel; i++){
            memcpy(csr+ptr[i].start, g->csr[i].data(), g->csr[i].size()*sizeof(uint16_t));
            memcpy(weight+ptr[i].start, g->weight[i].data(), g->weight[i].size()*sizeof(uint8_t));
        }
        MCTSNode* parent_ = parent;
        MCTSNode* child_ = this;
        while(parent_!=nullptr){
            for(int i = ptr[parent_->cur].start; i < ptr[parent_->cur].end; i++){
                if(csr[i] == child_->cur){
                    if (weight[i] > 0){
                        weight[i]--;
                        if(weight[i] == 0){
                            for(int j = i; j < ptr[parent_->cur].end-1; j++){
                                csr[j] = csr[j+1];
                                weight[j] = weight[j+1];
                            }
                            ptr[parent_->cur].end--;
                            assert(ptr[parent_->cur].end >= ptr[parent_->cur].start);
                        }
                        break;
                    }
                    assert(0);
                }
            }
            child_ = parent_;
            parent_ = parent_->parent;
        }
        int cur_ = cur;
        int player_ = player;
        int r = 0;
        if(ptr[cur_].start == ptr[cur_].end)
            r = -player_;
        int steps = 0;
        while(!r && steps < depth){
            int next_ = csr[ptr[cur_].start+(rand_r(&seed)%(ptr[cur_].end - ptr[cur_].start))];
            for(int i = ptr[cur_].start; i < ptr[cur_].end; i++){
                if(csr[i] == next_){
                    if (weight[i] > 0){
                        weight[i]--;
                        if(weight[i] == 0){
                            for(int j = i; j < ptr[cur_].end-1; j++){
                                csr[j] = csr[j+1];
                                weight[j] = weight[j+1];
                            }
                            ptr[cur_].end--;
                            assert(ptr[cur_].end >= ptr[cur_].start);
                        }
                        break;
                    }
                    assert(0);
                }
            }
            cur_ = next_;
            player_ = -player_;
            r = 0;
            if(ptr[cur_].start == ptr[cur_].end)
                r = -player_;
            steps++;
        }
        return r;
    }
    void BackPropagate(int result){
        q += result*player;
        n += 1;
        if(parent){
            parent->BackPropagate(result);
        }
    }
    int GetBestAction(){
        MCTSNode* best_child = UCT(bUCT);
        return best_child->cur;
    }
    shared_ptr<MCTSNode> GetChild(int next){
        for(auto c:child){
            if(c->cur == next){
                return c;
            }
        }
        for(auto move:GetKernelAvail()){
            if(move == next){
                Expand(next);
                return child.back();
            }
        }
        assert(0);
    }
    void MakeRoot(){
        parent = nullptr;
    }
    const vector<uint16_t>& GetKernelAvail(){
        if(!avail){
            vector<uint16_t> possibleAvail = g->csr[cur];
            vector<int8_t> possibleWeight = g->weight[cur];
            MCTSNode* parent_ = parent;
            MCTSNode* child_ = this;
            while(parent_ != nullptr){
                if(parent_->cur == cur){
                    for(size_t i = 0; i < possibleAvail.size(); i++){
                        if(possibleAvail[i] == child_->cur){
                            possibleWeight[i]--;
                            if (possibleWeight[i] == 0){
                                possibleAvail.erase(possibleAvail.begin()+i);
                                possibleWeight.erase(possibleWeight.begin()+i);
                            }
                            break;
                        }
                    }
                }
                child_ = parent_;
                parent_ = parent_->parent;
            }
            avail = make_shared<vector<uint16_t>>(possibleAvail);
        }
        return *avail;
    }
    bool isKernelTerminal(){
        return GetKernelAvail().size() == 0;
    }
    int cur;
    int player;
private:
    MCTSNode* UCT(float c){
        assert(child.size()!=0);
        float max = -numeric_limits<float>::max();
        MCTSNode* best_child = nullptr;
        for(size_t i = 0; i < child.size(); i++){
            float weight = -child[i]->q/child[i]->n + c*sqrt(log(n)/child[i]->n);
            if(weight > max){
                max = weight;
                best_child = child[i].get();
            }
        }
        assert(best_child != nullptr);
        return best_child;
    }
    void Expand(int next){
        shared_ptr<MCTSNode> node = make_shared<MCTSNode>(g, next, -player, this, seed);
        child.push_back(node);
    }
    Graph<nkernel>* g;
    MCTSNode* parent;
    float q;
    int n;
    uint32_t seed;
    vector<shared_ptr<MCTSNode>> child;
    shared_ptr<vector<uint16_t>> avail;
};

class Ladder{
public:
    Ladder(int cur_, int player_, uint32_t seed_):
        cur(cur_), player(player_){
        root = make_shared<MCTSNode>(&gkernel, cur_, player_, nullptr, seed_);
    }
    int LadderSearch(int visits){
        if(cur >= nkernel && cur < nkernel+nwin){
            for(auto move:GetLadderAvail()){
                if(move >= nkernel+nwin)
                    return move;
            }
            assert(0);
        }else if(cur < nkernel && !root->isKernelTerminal()){
            for(int i = 0; i < visits; i++){
                MCTSNode* c = root->SelectExpand();
                c->BackPropagate(c->Rollout());
            }
            return root->GetBestAction();
        }else if(!isLadderTerminal()){
            for(auto move:GetLadderAvail()){
                return move;
            }
        }
        assert(0);
    }
    void LadderMove(int next){
        if(next < nkernel){
            root = root->GetChild(next);
            gkernel.Decrease(cur, next);
            root->MakeRoot();
        }
        assert(!isLadderTerminal());
        gtotal.Decrease(cur, next);
        cur = next;
        player = -player;
    }
    const vector<uint16_t>& GetLadderAvail(){
        return gtotal.csr[cur];
    }
    bool isLadderTerminal(){
        return GetLadderAvail().size() == 0;
    }
    int GetLadderResult(){
        if(isLadderTerminal())
            return -player;
        return 0;
    }
    int cur;
    int player;
private:
    Graph<nkernel> gkernel;
    Graph<ntotal> gtotal;
    shared_ptr<MCTSNode> root;
};

extern "C"
{
    Ladder* ladder_init(int cur, int seed){return new Ladder(cur,1,seed);}
    int ladder_search(Ladder* l){return l->LadderSearch(playouts);}
    void ladder_move(Ladder* l, int n){l->LadderMove(n);}
    int ladder_result(Ladder* l){return l->GetLadderResult();}
    void ladder_destroy(Ladder* l){delete l;}
}